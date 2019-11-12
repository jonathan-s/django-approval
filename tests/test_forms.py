#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase, RequestFactory
from django.core.serializers import serialize

from django_approval import models
from django_approval import choices
from django_approval.test_utils import factories as factory
from django_approval.test_utils.test_app import forms
from django_approval.test_utils.test_app.models import Child


class UsingApprovalFormTest(TestCase):

    def setUp(self):
        self.initial = {
            'field1': 'hello',
            'field2': 'world'
        }
        self.request = RequestFactory()
        self.form = forms.ChildModelForm(self.initial, request=self.request)

    def test_approval_is_created_when_using_approval_form(self):
        '''An approval instance is created instead of Child instance
        since this form will prevent any creation of TestModels'''

        self.assertEqual(self.form.is_valid(), True, self.form.errors)
        test_inst = Child(**self.initial)
        serialized = serialize('json', [test_inst])
        instance = self.form.save()

        self.assertEqual(models.Approval.objects.count(), 1)
        self.assertEqual(isinstance(instance, models.Approval), True)
        self.assertJSONEqual(serialized, instance.source)
        self.assertEqual(instance.status, choices.Status.none)
        self.assertEqual(instance.action, choices.Action.create)
        self.assertEqual(instance.object_id, None)
        self.assertEqual(instance.content_object, None)

    def test_approval_for_existing_object(self):
        '''An existing object will create an approval to update that object'''
        test_inst = Child(**self.initial)
        test_inst.save()
        data = {'field1': 'update', 'field2': 'update2'}
        updated_obj = Child(id=test_inst.pk, **data)
        serialized = serialize('json', [updated_obj])
        form = forms.ChildModelForm(data=data, instance=test_inst)

        self.assertEqual(form.is_valid(), True, form.errors)
        instance = form.save()

        self.assertEqual(models.Approval.objects.count(), 1)
        self.assertEqual(isinstance(instance, models.Approval), True)
        self.assertEqual(instance.status, choices.Status.none)
        self.assertEqual(instance.action, choices.Action.update)
        self.assertEqual(instance.object_id, test_inst.pk)
        self.assertEqual(instance.content_object, test_inst)
        self.assertJSONEqual(serialized, instance.source)

    def test_form_can_handle_request_argument(self):
        '''The form allows a request argument'''
        self.assertEqual(self.form.request, self.request)

    def test_approval_with_partial_update(self):
        '''Form contains partial data for an update, no fields are overwritten'''
        pass

    def test_be_able_to_leave_a_comment_through_the_form(self):
        pass
