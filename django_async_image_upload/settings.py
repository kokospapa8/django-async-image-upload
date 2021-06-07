# coding: utf-8

# DJANGO IMPORTS
from django.conf import settings


BUCKET = getattr(settings, "ASYNC_IMAGE_UPLOAD_BUCKET", None)
BUCKET = getattr(settings, "ASYNC_IMAGE_UPLOAD_BUCKET", 'daas-dev-thumbnail')
TEMPORARY_IMAGE_PATH = getattr(settings, "ASYNC_IMAGE_UPLOAD_TEMPORARY_IMAGE_PATH", "temp/")
PRESIGNED_URL_EXPIRATION = getattr(settings,
                                   "ASYNC_IMAGE_UPLOAD_PRESIGNED_URL_EXPIRATION", 1000)
PRESIGNED_URL_REUSE_WINDOW = getattr(settings,
                                     "ASYNC_IMAGE_UPLOAD_PRESIGNED_URL_REUSE_WINDOW", 30)

PRESIGNED_URL_CONTENT_LENGTH = getattr(settings,
                                     "ASYNC_IMAGE_UPLOAD_PRESIGNED_URL_CONTENT_LENGTH", 10485760) # 10MiB
PROCESSED_IMAGE_MODEL = getattr(settings,
                             "PROCESSED_IMAGE_MODEL", "ProcessedImage")
