=====
Usage
=====

To use Django approval in a project, add it to your `INSTALLED_APPS`:

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
