=====
Usage
=====

To use Django-async-image-upload in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_async_image_upload.apps.AsyncImageUploadAppConfig',
        ...
    )

Add Django-async-image-upload's URL patterns:

.. code-block:: python

    from django_async_image_upload import urls as django_async_image_upload_urls


    urlpatterns = [
        ...
        url(r'^', include(django_async_image_upload_urls)),
        ...
    ]
