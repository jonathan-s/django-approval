from django.contrib import admin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin


class ApprovalInlineModelAdmin(GenericInlineModelAdmin):
    pass
    # we need to change the formset.
    # I think we need to change the formset.
    # formset = BaseGenericInlineFormSetpass

    # the formset actually only shows us objects for our target object.


class ApprovalStackedInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class ApprovalTabularInline(ApprovalInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'


class ApprovalAdmin(admin.ModelAdmin):
    '''
    The admin that would contain all approvals for all models.

    Should be able to filter by model or similar in list view.

    This will contain a view for approve / reject for a certain approval object.


    This needs to be in common with approval inline model admin too.

    This will add a field with a link Approve / Reject

    The link sends a get request that updates the approval object associated
    with our target object. That then creates the real object if approved.

    When clicking approve or reject. We know which approval object that we should
    update from. But when the approval object is in "update", there may be
    several "updates" that are conflicting for target object.

    So if we approve an update, all other updates for target object should be
    rejected.

    '''
    pass


class ApprovalMixin:
    '''
    Add this to your modeladmin or inline model admin for the model that needs
    approvals.

    This adds a delete link that will create a delete approval for that object.
    '''
    pass
