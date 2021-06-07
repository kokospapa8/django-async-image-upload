import boto3
import logging
import uuid

from botocore.exceptions import ClientError

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

from .settings import PRESIGNED_URL_CONTENT_LENGTH, TEMPORARY_IMAGE_PATH

logger = logging.getLogger(__name__)


def generate_upload_key():
    return uuid.uuid4().hex


def generate_presigned_url(bucket, key, expiration, metadata):
    try:
        s3_client = boto3.client('s3')

        conditions = [
            {"acl": "bucket-owner-full-control"},
            ["starts-with", "$key", TEMPORARY_IMAGE_PATH],
            ["starts-with", "$Content-Type", "image/"],
            ["content-length-range", 0, PRESIGNED_URL_CONTENT_LENGTH]
        ]

        fields = {
             "Content-Type": "image/*",
             "acl": "bucket-owner-full-control"
         }
        for k, v in metadata.items():
            fields[f"x-amz-meta-{k}"] = v
            conditions.append(
                {f"x-amz-meta-{k}": v}
            )

        response = s3_client.generate_presigned_post(bucket, key,
                                                     Conditions=conditions,
                                                     Fields=fields,
                                                     ExpiresIn=expiration,
                                                     )
        return response
    except ClientError as e:
        logger.error(f"error generating presigned url: {e}")
        logger.error(f"params bucket: {bucket}")
        logger.error(f"params bucket: {key}")
        logger.error(f"params bucket: {fields}")
        logger.error(f"params bucket: {conditions}")
        logger.error(f"params bucket: {expiration}")
        raise e


def get_image_model():
    """
    Return the image model that is active in this project.
    """
    try:
        from .settings import PROCESSED_IMAGE_MODEL
        # return apps.get_model(PROCESSED_IMAGE_MODEL, require_ready=False)
        return apps.get_model('async_image_upload', model_name=PROCESSED_IMAGE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PROCESSED_IMAGE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "PROCESSED_IMAGE_MODEL refers to model '%s' that has not been installed" % PROCESSED_IMAGE_MODEL
        )

