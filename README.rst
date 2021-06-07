=============================
Django-async-image-upload
=============================

.. image:: https://badge.fury.io/py/django-async-image-upload.svg
    :target: https://badge.fury.io/py/django-async-image-upload

.. image:: https://travis-ci.org/kokospapa8/django-async-image-upload.svg?branch=master
    :target: https://travis-ci.org/kokospapa8/django-async-image-upload

.. image:: https://codecov.io/gh/kokospapa8/django-async-image-upload/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kokospapa8/django-async-image-upload

Async image upload using presigned url for Django

Provide async extensibility of cloud architecture with image processing

There are good image upload solutions such as Sorl-thumb, etc. but these all synchrounous that the server needs to accept all the image file (even though image processing is done behind scene such as using celery and still needs to be uploaded to S3 again)
Using s3 presigned-url feature, client directly uploads to S3 (preferably closer region) without involving backend server. This way, api server waits for upload finish signal either from a) the client or b) s3 event notification

current version only provide asynchronous upload but in future it will provide connectivities using SNS and event bus.

Documentation
-------------

The full documentation is at https://django-async-image-upload.readthedocs.io.

Prerequisite
----------
- Django 3.1 due to Json field
- DB: MariaDB 10.2.7+, MySQL 5.7.8+, Oracle, PostgreSQL, and SQLite


Quickstart
----------

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
