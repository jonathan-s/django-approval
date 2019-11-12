from urllib.parse import urlencode

from django.apps import apps
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_approval.models import Approval
from django_approval.choices import Status

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


class ApprovalInlineModelAdmin(GenericInlineModelAdmin):
    '''To show approvals as inlines you need to inherit from this'''
    parent_fk = None

    def __init__(self, *args, **kwargs):
        if not self.parent_fk:
            # we might be able to figure this one out.
            # because we have self.model
            # can we get page we are at here somewhere...
            # assume that we have an attribute current_pk
            raise RuntimeError('We need the name of the relation')
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
        pk = request.GET.get('approval_id')
        obj = Approval.objects.get(pk=pk)
        obj.reject(user=request.user)

        # how do we redirect back...
        name = 'admin:' + get_admin_name(self.model, 'change')
        return redirect(name, self.current_pk)

    def approve(self, request, *args, **kwargs):
        pk = request.GET.get('approval_id')
        obj = Approval.objects.get(pk=pk)
        obj.approve(user=request.user)

        # how do we redirect back...
        name = 'admin:' + get_admin_name(self.model, 'change')
        return redirect(name, self.current_pk)

    # we need to change the formset.
    # I think we need to change the formset.
    # formset = BaseGenericInlineFormSetpass

    # the formset actually only shows us objects for our target object.


class ApprovalStackedInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class ApprovalTabularInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
    parent_inline_model = None

    def __init__(self, *args, **kwargs):
        if self.parent_inline_model is None:
            msg = _('You need to specify parent_inline_model')
            raise RuntimeError(msg)
        super().__init__(*args, **kwargs)

    @mark_safe
    def approval(self, obj):
        approve_url = reverse_admin_name(
            self.parent_inline_model,
            name=APPROVE_NAME,
            kwargs={'approval_id': obj.pk}
        )
        reject_url = reverse_admin_name(
            self.parent_inline_model,
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


class ApprovalAdmin(admin.ModelAdmin):
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
