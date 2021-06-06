=============================
Django-async-image-upload
=============================

.. image:: https://badge.fury.io/py/django-async-image-upload.svg
    :target: https://badge.fury.io/py/django-async-image-upload

.. image:: https://travis-ci.org/kokospapa8/django-async-image-upload.svg?branch=master
    :target: https://travis-ci.org/kokospapa8/django-async-image-upload

.. image:: https://codecov.io/gh/kokospapa8/django-async-image-upload/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kokospapa8/django-async-image-upload

Your project description goes here

Documentation
-------------

The full documentation is at https://django-async-image-upload.readthedocs.io.

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
