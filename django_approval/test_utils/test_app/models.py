from django.db import models
from django_approval.models import ApprovableModelMixin


class Parent(models.Model):
    name = models.CharField(max_length=16)


class Child(models.Model, ApprovableModelMixin):
    field1 = models.CharField(max_length=32)
    field2 = models.CharField(max_length=32)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
