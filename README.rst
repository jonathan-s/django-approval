=============================
Django approval
=============================

.. image:: https://badge.fury.io/py/django-approval.svg
    :target: https://badge.fury.io/py/django-approval

.. image:: https://travis-ci.org/jonathan-s/django-approval.svg?branch=master
    :target: https://travis-ci.org/jonathan-s/django-approval

.. image:: https://codecov.io/gh/jonathan-s/django-approval/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jonathan-s/django-approval

Use this for models that require approvals before being saved

Documentation
-------------

The full documentation is at https://django-approval.readthedocs.io.

Quickstart
----------

Install Django approval::

    pip install django-approval

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_approval.apps.DjangoApprovalConfig',
        ...
    )

Add Django approval's URL patterns:

.. code-block:: python

    from django_approval import urls as django_approval_urls


    urlpatterns = [
        ...
        url(r'^', include(django_approval_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
