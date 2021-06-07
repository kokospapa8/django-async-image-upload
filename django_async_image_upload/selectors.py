import datetime
from typing import Union, List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import PresignedUrl

User = get_user_model()


def get_unexpired_presigned_url_instance(user: User, time_window: datetime) \
        -> Union[PresignedUrl, None]:
    try:
        return get_unexpired_presigned_url_list(user, time_window)[0]
    except IndexError:
        return None


def get_unexpired_presigned_url_list(user: User, time_window: datetime) \
        -> Union[QuerySet, List[PresignedUrl]]:
    return PresignedUrl.objects.filter(
        user=user,
        timestamp_expire__gte=time_window,
        timestamp_completed__isnull=True
    )

