=============================
Django approval
=============================

.. image:: https://badge.fury.io/py/django-approval.svg
    :target: https://badge.fury.io/py/django-approval

.. image:: https://travis-ci.org/jonathan-s/django-approval.svg?branch=master
    :target: https://travis-ci.org/jonathan-s/django-approval

.. image:: https://codecov.io/gh/jonathan-s/django-approval/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonathan-s/django-approval

Some data may require an approval before it is added to the database. The django-approvals apps is intended to provide a light-weight way of adding approvals to your app.

There is one table where all approvals exist for all models, through django's contenttype framework it's possible to differentiate an approval that belongs to one model from an approval that belongs to another model.


Interesting in getting more?
---------------------------

File an issue if there is anything you think is missing.
I'm also open for freelancing or contracting.


Documentation
-------------

Create a model that is approvable. In this case we want the wheels to be approvable.

.. code-block:: python

    from django.db import models
    from django_approval.models import ApprovableModelMixin

    class Car(models.Model):
        field1 = models.CharField(max_length=16)


    class Wheel(models.Model, ApprovableModelMixin):
        type = models.CharField(max_length=16)
        car = models.ForeignKey(Car, on_delete=models.CASCADE)


To trigger an approval use the approval form. It inherits from ModelForm, and when saved instead of saving an instance of a Wheel, it would save an instance of an Approval.

The form optionally takes a request parameter which is used to determine an author of the change.


.. code-block:: python

    from django_approval.form import FormUsingApproval

    class WheelModelForm(FormUsingApproval):

        class Meta:
            model = Wheel
            fields = '__all__'


An approval admin is automatically registered. All approvals for all models will be visible there. You can also add an approval inline admin if there is a foreign key relationship similar to `Car` and `Wheel` above.

All `Wheel` approvals that can be traced to have an association with a particular `Car` will be presented in one section for an overview. Here approvals can be made.

.. code-block:: python

    from django_approval.admin import ParentApprovalAdmin,
    from django_approval.admin import ApprovalTabularInline

    class WheelApprovalAdmin(ApprovalTabularInline):
        approval_for = Wheel


    @admin.register(models.Parent)
    class CarAdmin(ParentApprovalAdmin):
        inlines = [
            WheelApprovalAdmin
        ]


Quickstart
----------

Install Django approval (not yet on pypi)::

    pip install django-approval

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_approval',
        ...
    )


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox
