# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import PresignedUrl


class PresignedUrlAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'user', 'timestamp_created', 'timestamp_completed']
    raw_id_fields = ['user']
    list_filter = ['timestamp_completed']


admin.site.register(PresignedUrl, PresignedUrlAdmin)

