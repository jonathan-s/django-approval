from django import forms


class ModelUsingApprovalForm(forms.ModelForm):

    def need_approval(self):
        """By default we always need approval when using this form"""
        return True

    def save():
        """can compare initial with cleaned_data

        do a diff of all fields in the dictionary and save the html output
        the self.initial may contain fewer fields than self.cleaned_data.
        only compare the fields provided by self.initial

        Consider that you might need to be able to compare foreign keys.

        A signal should be created when an approval is created.
        A signal for each type; create, update, delete.
        """
        pass


