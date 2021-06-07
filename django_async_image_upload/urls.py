# coding: utf-8
from django.urls import path

from rest_framework.routers import SimpleRouter

from .docs import get_schema_view_from_urlpatterns
from .viewsets import PresignedUrlViewSet, ProcessedImageViewSet

router = SimpleRouter()
router.register(r'presigned_urls', PresignedUrlViewSet, basename='presigned_url')
router.register(r'processed_images', ProcessedImageViewSet, basename='processed_image')

urlpatterns = router.urls

async_image_upload_doc = get_schema_view_from_urlpatterns(
    router.urls, "async_image_upload/"
)

urlpatterns += [
    path('docs/swagger', async_image_upload_doc.with_ui('swagger', cache_timeout=0),
         name='async_image_upload_swagger'),

]
