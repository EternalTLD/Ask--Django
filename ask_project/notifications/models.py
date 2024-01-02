from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationManager(models.query.QuerySet):
    """Notification manager"""

    def unread(self):
        """Returns query set of unread notifications"""
        qs = self.filter(is_read=False)
        return qs

    def mark_all_as_read(self):
        """Marks unread notifications as read and returns them"""
        qs = self.unread()
        qs.update(is_read=True)
        return qs


class Notification(models.Model):
    """Notification model"""

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_notifications",
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    message = models.CharField(null=True, max_length=50)
    url = models.URLField(null=True)

    objects = NotificationManager.as_manager()

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.message

    def mark_as_read(self) -> bool:
        self.is_read = True
        self.save()
        return True


@receiver(post_save, sender=Notification)
def notification_handler(**kwargs) -> None:
    """Handler to send notification"""
    instance = kwargs.pop("instance")
    if kwargs.pop("created"):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_{instance.to_user.username}",
            {
                "type": "send_notification",
                "notification": {
                    "message": instance.message,
                    "created_at": instance.created_at.strftime("%Y-%m-%d %H:%m"),
                    "url": instance.url,
                },
            },
        )
