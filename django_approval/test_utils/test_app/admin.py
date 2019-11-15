from django.contrib import admin

from django_approval.test_utils.test_app import models
from django_approval.admin import ApprovalTabularInline
from django_approval.admin import ParentApprovalAdmin


class ChildApprovalAdmin(ApprovalTabularInline):
    approval_for = models.Child


@admin.register(models.Child)
class ChildAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Parent)
class ParentAdmin(ParentApprovalAdmin):
    inlines = [
        ChildApprovalAdmin
    ]
