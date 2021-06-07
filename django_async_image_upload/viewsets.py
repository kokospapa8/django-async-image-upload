import datetime

from django.utils import timezone

from rest_framework import viewsets, permissions

from . import settings
from .docs import doc_presigned_url_create, doc_presigned_url_update
from .models import (
    PresignedUrl,
    ProcessedImage
    )
from .permissions import PresignedUrlViewPermission
from .selectors import get_unexpired_presigned_url_list
from .serializers import (
    PresignedUrlSerialzier,
    PresignedUrlCreateSerialzier,
    PresignedUrlUpdateSerialzier
    )


class PresignedUrlViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    serializer_class = PresignedUrlSerialzier
    queryset = PresignedUrl.objects.all()
    http_method_names = ['get', 'post', 'head', 'put']
    permission_classes = [PresignedUrlViewPermission]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = PresignedUrlCreateSerialzier
        if self.request.method == 'PUT':
            serializer_class = PresignedUrlUpdateSerialzier
        return serializer_class

    def get_queryset(self):
        time_window = timezone.now() + \
                     datetime.timedelta(seconds=settings.PRESIGNED_URL_REUSE_WINDOW)
        return get_unexpired_presigned_url_list(self.request.user, time_window)

    @doc_presigned_url_create
    def create(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @doc_presigned_url_update
    def update(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProcessedImageViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    serializer_class = PresignedUrlSerialzier
    queryset = ProcessedImage.objects.all()
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'list', 'head']
