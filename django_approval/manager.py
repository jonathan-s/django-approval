from django.apps import apps
from django.db import models
from django.contrib.contenttypes.models import ContentType


class ApprovalQueryset(models.QuerySet):
    def for_model(self, model, queryset=None):
        if queryset is None:
            queryset = model.objects.all()
        content_type = ContentType.objects.get_for_model(model)
        # it would be preferable to do a join here if possible
        return self.filter(
            content_type__pk=content_type.pk, object_id__in=queryset
        )


class ApprovalManager(models.Manager):
    def get_queryset(self):
        return ApprovalQueryset(self.model, using=self._db)

    def for_model(self, model, queryset=None):
        return self.get_queryset().for_model(model=self.model, queryset=queryset)

    def get_object(self, model, object_id):
        content_type = ContentType.objects.get_for_model(model)
        Model = apps.get_model(content_type.app_name, content_type.model)
        return Model.objects.get(pk=object_id)


class ApprovableQueryset(models.QuerySet):
    pass
