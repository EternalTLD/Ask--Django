from django.db import models
from django.conf import settings
from django.utils import timezone


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

    def to_json(self) -> dict:
        return {
            "to_user_username": self.to_user.username,
            "to_user_email": self.to_user.email,
            "message": self.message,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%m"),
            "url": self.url,
        }
