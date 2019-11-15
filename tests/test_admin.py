#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.core.serializers import serialize
from django.test import TestCase
from django.test import RequestFactory

from django_approval.admin import reverse_admin_name
from django_approval.admin import APPROVE_NAME, REJECT_NAME
from django_approval.choices import Status

from django_approval.test_utils import factories as factory
from django_approval.test_utils.test_app import models as test_models
from django_approval.test_utils.test_app import admin

request = RequestFactory()


class ApprovalAdminTest(TestCase):

    def setUp(self):
        self.parent = factory.ParentFactory()
        self.data = {'field1': 'test1', 'field2': 'test2', 'parent_id': self.parent.pk}
        instance = test_models.Child(**self.data)
        serialized = serialize('python', [instance])
        self.approval = factory.ChildApprovalFactory()
        self.test_inst = test_models.Child.objects.first()
        self.user = factory.UserFactory()

        self.approval.object_id = None
        self.approval.source = serialized
        self.approval.save()

        self.kwargs = {'approval_id': self.approval.pk}
        self.approve_url = reverse_admin_name(
            test_models.Parent, APPROVE_NAME, kwargs=self.kwargs
        )

        self.parent_url = reverse_admin_name(
            test_models.Parent, 'change', kwargs={'object_id': self.parent.pk}
        )
        self.client.force_login(self.user)

    def test_approva_approval_view(self):
        '''Approves the approval and redirect back'''
        self.client.get(self.parent_url)
        resp = self.client.get(self.approve_url)
        self.approval.refresh_from_db()

        self.assertEqual(self.approval.status, Status.approved)
        self.assertRedirects(resp, self.parent_url)

    def test_reject_approval_view(self):
        '''Rejects the approval and redirect back'''
        reject_url = reverse_admin_name(
            test_models.Parent, REJECT_NAME, kwargs=self.kwargs
        )
        self.client.get(self.parent_url)
        resp = self.client.get(reject_url)
        self.approval.refresh_from_db()

        self.assertEqual(self.approval.status, Status.rejected)
        self.assertRedirects(resp, self.parent_url)

    def test_current_pk_is_set_when_accessing_object(self):
        '''Inlined admins has no knowledge of parent, this way parent knows
        about what the current change view object is.
        '''
        site = AdminSite()
        parentadmin = admin.ParentAdmin(test_models.Parent, site)
        obj = parentadmin.get_object(request, self.parent.pk)

        self.assertEqual(parentadmin.current_pk, obj.pk)


class InlineApproval(TestCase):
    def setUp(self):
        self.approval = factory.ChildApprovalFactory()
        self.other_approval = factory.ChildApprovalFactory()
        self.child = self.approval.content_object
        self.parent = self.child.parent

        self.second_approval = factory.ChildApprovalFactory()
        self.second_approval.content_object.parent_id = self.parent.pk
        self.second_approval.content_object.save()

        self.parent_url = reverse_admin_name(
            test_models.Parent, 'change', kwargs={'object_id': self.parent.pk}
        )

        self.user = factory.UserFactory()
        self.client.force_login(self.user)

    def test_inline_queryset(self):
        '''Two different child pks are shown in the same approval with the same parent, child with different parent is excluded'''
        site = AdminSite()
        self.approval
        get_request = request.get(self.parent_url)
        get_request.user = self.user
        inline = admin.ChildApprovalAdmin(test_models.Parent, site)

        qs = inline.get_queryset(get_request)
        self.assertEquals(qs.count(), 2)
