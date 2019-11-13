from urllib.parse import urlencode

from django.apps import apps
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_approval.models import Approval
from django_approval.choices import Status
from django_approval import forms

APPROVE_NAME = 'approve'
REJECT_NAME = 'reject'


def get_admin_name(model, name):
    if isinstance(model, str):
        app_name, model_name = model.split('.')
        model = apps.get_model(app_name, model_name)

    name = '{}_{}_{}'.format(
        model._meta.app_label,
        model._meta.model_name,
        name
    )
    return name


def reverse_admin_name(model, name, args=None, kwargs=None, params=None):
    if isinstance(model, str):
        app_name, model_name = model.split('.')
        model = apps.get_model(app_name, model_name)

    name = get_admin_name(model, name)
    url = reverse('admin:{}'.format(name), args=args, kwargs=kwargs)
    if params:
        url = f'{url}?{urlencode(params)}'
    return url


class ParentApprovalAdmin(admin.ModelAdmin):
    '''ParentApprovalAdmin allows you to have inline modeladmins that uses approvals'''
    parent_fk = None

    def __init__(self, *args, **kwargs):
        if not self.parent_fk:
            pass
            # we might be able to figure this one out.
            # because we have self.model
            # can we get page we are at here somewhere...
            # assume that we have an attribute current_pk
            # raise RuntimeError('We need the name of the relation')
        super().__init__(*args, **kwargs)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        added_urls = [
            path(
                'approve/<approval_id>/',
                self.approve,
                name=get_admin_name(self.model, APPROVE_NAME)
            ),
            path(
                'reject/<approval_id>/',
                self.reject,
                name=get_admin_name(self.model, REJECT_NAME)
            )
        ]
        # order is important !!
        return added_urls + urls

    def reject(self, request, *args, **kwargs):
        pk = kwargs.get('approval_id')
        obj = Approval.objects.get(pk=pk)
        obj.reject(user=request.user)

        # how do we redirect back...
        name = 'admin:' + get_admin_name(self.model, 'change')
        return redirect(name, self.current_pk)

    def approve(self, request, *args, **kwargs):
        pk = kwargs.get('approval_id')
        obj = Approval.objects.get(pk=pk)
        obj.approve(user=request.user)

        # how do we redirect back...
        name = 'admin:' + get_admin_name(self.model, 'change')
        return redirect(name, self.current_pk)


class ApprovalInlineModelAdmin(GenericInlineModelAdmin):
    formset = forms.ApprovalGenericInlineFormset

    approval_for = None

    def __init__(self, *args, **kwargs):
        if self.approval_for is None:
            msg = _('You need to specify: approval_for, the model for which this is an approval')
            raise RuntimeError(msg)
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        def get_field_names(fields):
            for field in fields:
                if field.is_relation and hasattr(field.related_model, 'approvals'):
                    yield (field.related_model, field.remote_field.name)

        resolved = resolve(request.path)
        object_id = resolved.kwargs['object_id']

        # removes the actual name of view
        app = resolved.url_name.split('_')[:-1]

        # assumption is that there will never be underscores in class names
        model_name = app[-1]
        app_name = '_'.join(app[:-1])

        self.ParentModel = apps.get_model(app_name, model_name)
        fields = self.ParentModel._meta.get_fields(include_hidden=True)
        model_queryset = [
            (Model, Model.objects.filter(**{'{}_id'.format(name): object_id}))
            for (Model, name) in get_field_names(fields)
            if Model == self.approval_for
        ]
        assert(len(model_queryset), 1, 'There should only ever be one model with the same name')
        Model, queryset = model_queryset[0]
        content_type = ContentType.objects.get_for_model(Model)

        qs = super().get_queryset(request)
        # above queryset gives us all approvals, we filter out all approvals
        # except the ones related to the model in `approval_for`
        qs = qs.filter(**{
            self.ct_field: content_type,
            '{}__in'.format(self.ct_fk_field): queryset,
        })
        return qs

    @mark_safe
    def approval(self, obj):
        approve_url = reverse_admin_name(
            self.ParentModel,
            name=APPROVE_NAME,
            kwargs={'approval_id': obj.pk}
        )
        reject_url = reverse_admin_name(
            self.ParentModel,
            name=REJECT_NAME,
            kwargs={'approval_id': obj.pk}
        )
        approve_text = _('Approve')
        reject_text = _('Reject')
        approve = f'<a href="{approve_url}">{approve_text}</a>'
        reject = f'<a href="{reject_url}">{reject_text}</a>'
        link = f'{approve} / {reject}'
        action_taken = any([
            obj.status == Status.rejected,
            obj.status == Status.approved
        ])
        if action_taken:
            return 'Action taken'
        return link
    approval.short_description = 'Decide'


class ApprovalStackedInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class ApprovalTabularInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'


class ApprovalModelAdmin(admin.ModelAdmin):
    '''
    The admin that would contain all approvals for all models.

    Should be able to filter by model or similar in list view.

    This will contain a view for approve / reject for a certain approval object.


    This needs to be in common with approval inline model admin too.

    This will add a field with a link Approve / Reject

    The link sends a get request that updates the approval object associated
    with our target object. That then creates the real object if approved.

    When clicking approve or reject. We know which approval object that we should
    update from. But when the approval object is in "update", there may be
    several "updates" that are conflicting for target object.

    So if we approve an update, all other updates for target object should be
    rejected.

    '''
    pass


class ApprovalMixin:
    '''
    Add this to your modeladmin or inline model admin for the model that needs
    approvals.

    This adds a delete link that will create a delete approval for that object.
    '''
    pass
