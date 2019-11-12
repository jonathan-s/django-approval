from django.db import models


class TestModel(models.Model):
    field1 = models.CharField(max_length=32)
    field2 = models.CharField(max_length=32)
