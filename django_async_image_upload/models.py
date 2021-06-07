import uuid
import dateutil

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PresignedUrl(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    credential = models.JSONField(default=dict)
    processed_key = models.CharField(max_length=256, blank=True)

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_expire = models.DateTimeField(null=True, blank=True)
    timestamp_completed = models.DateTimeField(null=True, blank=True, db_index=True)

    metadata = models.JSONField(default=dict)
    error = models.JSONField(default=None, null=True)

    class Meta:
        app_label = "async_image_upload"
        db_table = "presignedurl"
        ordering = ("-timestamp_created", "-timestamp_expire")

    def status(self):
        status = "created"
        if self.processed_key:
            status = "completed"
        elif self.error:
            status = "error"
        elif self.expired():
            status = "expired"

        return status

    def expired(self):
        # convert offset-naive to offset-aware
        time_expired = dateutil.parser.parse(self.timestamp_expire)
        time_expired = timezone.make_aware(time_expired)
        return True if timezone.now() > time_expired else False


class ProcessedImage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    processed_key = models.CharField(max_length=256, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        app_label = "async_image_upload"
        db_table = "processedimage"

    @classmethod
    def create_model(cls, *args, **kwargs):
        #do something with metadata if you need to
        dict_data = {
            "processed_key": kwargs['processed_key'],
            "user": kwargs['user'],
            "metadata": kwargs['metadata'],
            "uuid": kwargs['uuid']
        }
        cls.objects.create(dict_data)
