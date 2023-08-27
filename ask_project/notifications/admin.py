from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ('to_user', 'from_user')
    list_display = ('to_user', 'from_user',
                    'question', 'created_at', 'read_at', 'type')