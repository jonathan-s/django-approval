# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from .choices import Status
from .choices import Action


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
    # contains html output of a diff for all fields.
    # possibly we would like the diff to be compared with current
    # object to what is stored as a change.

    # there is no diff for new objects.
    diff = models.TextField()
    # change = models. json field, with all the changes per field.
    # change = what changed.

    class Meta:
        verbose_name = _('approval')
        verbose_name_plural = _('approvals')
        # can't determine any unique status.
        # status can occur several times.
        # unique_together = (('content_type', 'object_id', 'status'),)
        ordering = (
            'content_type__app_label',
            'content_type__model',
            'object_id'
        )

    def natural_key(self):
        return (self.object_id,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']

