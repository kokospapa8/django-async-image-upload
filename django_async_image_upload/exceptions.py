from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class PresignedUrlGenerationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Presigned URL Generation Error.')
    default_code = 'presigned_url_generation_error'