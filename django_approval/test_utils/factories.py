from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import factory

from django_approval.models import Approval
from django_approval.choices import Action, Status
from django_approval.test_utils.test_app.models import Child, Parent

CHILD_PATH = 'django_approval.test_utils.factories.ChildFactory'


class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'Adam'
    is_superuser = True
    is_staff = True

    class Meta:
        model = User


class ApprovalFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    action = Action.create
    status = Status.none
    source = {}

    class Meta:
        exclude = ['content_object']
        abstract = True


class ChildApprovalFactory(ApprovalFactory):
    content_object = factory.SubFactory(CHILD_PATH)

    class Meta:
        model = Approval


class ParentFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name-%04d' % n)

    class Meta:
        model = Parent


class ChildFactory(factory.django.DjangoModelFactory):
    field1 = factory.Sequence(lambda n: 'field1-%04d' % n)
    field2 = factory.Sequence(lambda n: 'field2-%04d' % n)
    parent = factory.SubFactory(ParentFactory)

    class Meta:
        model = Child

