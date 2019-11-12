from django.db import models


class Child(models.Model):
    field1 = models.CharField(max_length=32)
    field2 = models.CharField(max_length=32)


class Parent(models.Model):
    children = models.ForeignKey(Child, on_delete=models.CASCADE)

