from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .serializers import (
    PresignedUrlSerialzier,
    ProcessedImageSerializer
    )


def get_schema_view_from_urlpatterns(urlpatterns, base_path):
    patterns = [
        path(base_path, include(urlpatterns[:]))
    ]

    return get_schema_view(
        openapi.Info(
            title="Async Image Upload API",
            default_version='',
            description="Swagger Doc for Async Image Upload API",
            terms_of_service="",
            contact=openapi.Contact(email="kokos.papa8@gmail.com"),
            license=openapi.License(name=""),
        ),
        # url=f'https://{settings.ENV}api.delivus.co.kr',
        patterns=patterns,
        public=True,
        permission_classes=(permissions.IsAdminUser,),
    )


doc_presigned_url_create = swagger_auto_schema(
    operation_id='presiend_url_create',
    operation_description='Create presigned url \n'
                          'only use metadata',

    operation_summary="Create presigned url",
    responses={
        200: PresignedUrlSerialzier,
        400: 'Presigned url generation error',
    }
)

doc_presigned_url_update = swagger_auto_schema(
    operation_id='presiend_url_update',
    operation_description='Update presigned url info from callback\n'
                          'success - processed_key\n'
                          'fail - error',
    operation_summary="Update presigned url with success or fail from lambda",
    responses={
        200: PresignedUrlSerialzier,
        400: 'wrong paramters',
    }
)
