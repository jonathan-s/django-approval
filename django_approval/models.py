# -*- coding: utf-8 -*-
from django.apps import apps
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import deserialize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from .choices import Status
from .choices import Action
from .manager import ApprovalManager


User = get_user_model()


class Approval(TimeStampedModel):
    '''
    Action tells us what the approval object is about
    Status tells us whether the action was approved or rejected.
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # if we create an object, we don't yet have an object it is referring to.
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    action = models.CharField(choices=Action.choices, max_length=8)
    status = models.CharField(
        choices=Status.choices,
        max_length=8,
        default=Status.none,
        blank=True
    )
    comment = models.CharField(
        max_length=255,
        help_text=_('The reason for this change'),
        blank=True
    )
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = JSONField(encoder=DjangoJSONEncoder, help_text='The fields as they would be saved.')

    # contains html output of a diff for all fields.
    # possibly we would like the diff to be compared with current
    # object to what is stored as a change.
    # there is no diff for new objects.
    diff = models.TextField()
    # change = models. json field, with all the changes per field.
    # change = what changed.

    objects = ApprovalManager()

    class Meta:
        verbose_name = _('approval')
        verbose_name_plural = _('approvals')
        ordering = (
            'content_type__app_label',
            'content_type__model',
            'object_id'
        )

    def natural_key(self):
        return (self.object_id,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']

    def get_model(self):
        return apps.get_model(
            self.content_object.app_name, self.content_object.model
        )

    @transaction.atomic
    def approve(self, user=None):
        if self.action == Action.update and not self.object_id:
            msg = _('Inconsistent state: an update always need an object_id')
            raise ValueError(msg)

        if self.action == Action.delete:
            self.content_object.delete()
            self.object_id = None
            self.status = Status.approved
            self.save()
            return

        deserialized_obj = next(deserialize('json', self.source))
        obj = deserialized_obj.object
        obj.save()
        self.changed_by = user
        self.status = Status.approved
        self.object_id = obj.pk
        self.save()

    def reject(self, user=None):
        self.changed_by = user
        self.status = Status.rejected
        self.save()


class ApprovableModelMixin:
    approvals = GenericRelation(Approval)

