from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Approval
from .choices import Action, Status


class FormUsingApproval(forms.ModelForm):
    '''
    For any model that is using approvals it needs to inherit from this form.
    '''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def need_approval(self):
        """By default we always need approval when using this form"""
        return True

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

        content_type = ContentType.objects.get_for_model(self.Meta.model)
        action = Action.update if self.instance.pk else Action.new

        if self.need_approval():
            approval = Approval.objects.create(
                content_type=content_type,
                action=action,
                status=Status.none,
                comment='',  # fix this later
                source={},
                diff=''
            )
            self.instance = approval
        return super().save(commit=commit)


class ApprovalForm(forms.ModelForm):

    class Meta:
        model = Approval
        fields = '__all__'

    def save(self, commit=True):
        object_id = self.instance.object_id
        if commit is True and object_id:
            Model = self.instance.get_model()
            obj = Model.objects.get(pk=object_id)
            # fill all the other fields for instance.
            obj.save()
        if commit is True and not object_id:
            Model = self.instance.get_model()
            Model.objects.create()  # fill in all arguments from source
        return super().save(commit=commit)
