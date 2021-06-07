import datetime

from django.utils import timezone
from rest_framework import serializers

from . import settings
from .models import PresignedUrl
from .exceptions import PresignedUrlGenerationError
from .selectors import get_unexpired_presigned_url_instance
from .utils import generate_presigned_url, generate_upload_key, \
    get_image_model

ProcessedImageModel = get_image_model()


class PresignedUrlSerialzier(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PresignedUrl
        fields = ["uuid",
                  "credential",
                  "timestamp_expire",
                  "processed_key",
                  "error",
                  "status",
                  ]

    def get_status(self, obj):
        return obj.status()


class PresignedUrlUpdateSerialzier(PresignedUrlSerialzier):
    processed_key = serializers.CharField(write_only=True, allow_blank=True, required=False)
    error = serializers.JSONField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = PresignedUrl
        fields = ["processed_key",
                  "error",
                  ]

    def update(self, instance, validated_data):
        if "processed_key" in validated_data:
            validated_data['timestamp_completed'] = timezone.now()
        elif "error" in validated_data:
            pass

        instance = super().update(instance, validated_data)
        ProcessedImageModel.create_model(PresignedUrlSerialzier(instance).data)
        return instance


class PresignedUrlCreateSerialzier(PresignedUrlSerialzier):
    metadata = serializers.JSONField(default={})

    class Meta:
        model = PresignedUrl
        fields = ["metadata"]

    def create_presigned_instance(self, user, metadata):
        key = generate_upload_key()

        try:
            response = generate_presigned_url(
                settings.BUCKET,
                f"{settings.TEMPORARY_IMAGE_PATH}{key}",
                settings.PRESIGNED_URL_EXPIRATION,
                metadata
            )
        except Exception as e:
            raise PresignedUrlGenerationError(e)

        create_data = {
            "uuid": key,
            "user": user if user.is_authenticated else None,
            "credential": response,
            "timestamp_expire": str(
                datetime.datetime.now() +
                datetime.timedelta(seconds=settings.PRESIGNED_URL_EXPIRATION)),
            "metadata": metadata
        }
        instance = super().create(create_data)
        return instance

    def get_presigned_instance(self, user, metadata):

        time_window = timezone.now() + \
                     datetime.timedelta(seconds=settings.PRESIGNED_URL_REUSE_WINDOW)

        instance = get_unexpired_presigned_url_instance(user, time_window)
        return self.create_presigned_instance(user, metadata) if instance is None else instance

    def create(self, validated_data):
        user = self.context['request'].user
        instance = self.get_presigned_instance(user, validated_data['metadata'])
        return instance


class ProcessedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessedImageModel
        fields = "__all__"
