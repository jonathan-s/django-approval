from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.core.serializers import serialize

from .models import Approval
from .choices import Action, Status


class ApprovalGenericInlineFormset(BaseGenericInlineFormSet):
    '''The normal GenericInlineFormset gets in our way. We want to collect
    all approvals for a single inline formset in one slot.'''

    # it might be better to just inherit from basemodelformset instead

    def __init__(self, data=None, files=None, instance=None, save_as_new=False,
                 prefix=None, queryset=None, **kwargs):
        original_qs = queryset
        super().__init__(queryset=queryset, data=data, files=files, prefix=prefix, **kwargs)
        if self.model == Approval:
            # for approval we have an already modified queryset
            self.queryset = original_qs


class FormUsingApproval(forms.ModelForm):
    '''
    For any model that is using approvals it needs to inherit from this form.
    '''

    # should have a comment field here...?

    def __init__(self, *args, **kwargs):
        if not hasattr(self.Meta.model, 'approvals'):
            raise RuntimeError('Model does not inherit from ApprovableModelMixin')
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """can compare initial with cleaned_data

        do a diff of all fields in the dictionary and save the html output
        the self.initial may contain fewer fields than self.cleaned_data.
        only compare the fields provided by self.initial

        Consider that you might need to be able to compare foreign keys.

        A signal should be created when an approval is created.
        A signal for each type; create, update, delete.
        """

        # make a diff to figure out if there is a change.
        # if we don't have a pk for instance it's definitely a new
        user = getattr(self.request, 'user', None)

        content_type = ContentType.objects.get_for_model(self.Meta.model)
        action = Action.update if self.instance.pk else Action.create
        source = serialize('json', [self.instance])

        if self.Meta.model.need_approval(user):
            approval = Approval.objects.create(
                object_id=self.instance.pk,
                content_type=content_type,
                author=user,
                action=action,
                status=Status.none,
                comment='',  # fix this later
                source=source,
                diff=''
            )
            self.instance = approval
        return super().save(commit=commit)
