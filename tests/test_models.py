#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.serializers import serialize

from django_approval import models
from django_approval.choices import Status, Action
from django_approval.test_utils import factories as factory
from django_approval.test_utils.test_app.models import TestModel


class ApprovalModelTest(TestCase):

    def setUp(self):
        self.data = {'field1': 'test1', 'field2': 'test2'}
        instance = TestModel(**self.data)
        serialized = serialize('json', [instance])
        self.approval = factory.TestModelApprovalFactory()
        self.approval.object_id = None
        self.approval.source = serialized
        self.approval.save()

    def test_approve_approval(self):
        '''Changes the status method to approved and creates target object'''
        values = set(self.data.values())
        count = TestModel.objects.count()
        self.approval.approve()
        object_values = set(self.approval.content_object.__dict__.values())

        self.assertEqual(self.approval.status, Status.approved)
        self.assertEqual(values.issubset(object_values), True, (values, object_values))
        self.assertEqual(count + 1, TestModel.objects.count())
        self.assertIsNotNone(self.approval.object_id)

    def test_raise_inconsistent_error(self):
        '''If action is update, approval needs to contain object id'''
        self.approval.action = Action.update
        with self.assertRaises(ValueError):
            self.approval.approve()

    def test_reject_approval(self):
        '''Changes status to rejected, does not create anything; it was rejected'''
        count = TestModel.objects.count()
        self.approval.reject()

        self.assertEqual(self.approval.status, Status.rejected)
        self.assertEqual(count, TestModel.objects.count())

    def tearDown(self):
        pass
