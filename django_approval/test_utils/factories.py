from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import factory

from ..models import Approval


class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'Adam'

    class Meta:
        model = User


class ApprovalFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        exclude = ['content_object']
        abstract = True


# class TaggedUserFactory(TaggedItemFactory):
#     content_object = factory.SubFactory(UserFactory)

#     class Meta:
#         model = TaggedItem
