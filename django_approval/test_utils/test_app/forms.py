from django_approval.forms import FormUsingApproval
from django_approval.test_utils.test_app.models import TestModel


class TestModelForm(FormUsingApproval):

    class Meta:
        model = TestModel
        fields = '__all__'
