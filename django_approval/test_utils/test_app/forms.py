from django_approval.forms import FormUsingApproval
from django_approval.test_utils.test_app.models import Child


class ChildModelForm(FormUsingApproval):

    class Meta:
        model = Child
        fields = '__all__'
