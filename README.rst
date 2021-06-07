=============================
Django-async-image-upload
=============================

.. image:: https://badge.fury.io/py/django-async-image-upload.svg
    :target: https://badge.fury.io/py/django-async-image-upload


Async image upload using presigned url for Django.

This module provide async extensibility of cloud architecture with image processing

There are already plenty of good thumbnail packages such as [sorl-thumbnail](https://github.com/jazzband/sorl-thumbnail), [django-versatileimagefield](https://github.com/respondcreate/django-versatileimagefield_etc.
However most of the packages process image on django server. Some are partially asynchrounous with celery and other technique, but server still needs to recieve files from client to proecess them.

Using S3(and others storages in the futures) presigned-url feature, client can directly uploads to S3 without involving backend server.
Once image is uploaded, api server gets callback once image processing in finished elsewhere(serverless function in this case.

Current version only provide asynchronous upload but in future it will provide connectivities using SNS and event bus.

## Future

# Architecture




## Prerequisite
- Django 3.1 due to Json field
- DB: MariaDB 10.2.7+, MySQL 5.7.8+, Oracle, PostgreSQL, and SQLite


Quickstart
------------

Install Django-async-image-upload::

    pip install django-async-image-upload

Add it to your `INSTALLED_APPS`:

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


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
