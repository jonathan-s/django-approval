from django.contrib import admin

from django_approval.test_utils.test_app import models
from django_approval.admin import ApprovalTabularInline
from django_approval.admin import ParentApprovalAdmin
from django_approval.models import Approval


class ChildApprovalAdmin(ApprovalTabularInline):
    parent_inline_model = models.Parent
    model = Approval


@admin.register(models.Child)
class ChildAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Parent)
class ParentAdmin(ParentApprovalAdmin):
    inlines = [
        ChildApprovalAdmin
    ]

