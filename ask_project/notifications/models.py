from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from ask_project import settings


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
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='sent_notifications', 
        verbose_name='Отправитель',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='recieved_notifications', 
        verbose_name='Получатель'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Отправлено')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    sent = models.BooleanField(default=False, verbose_name='Отправлено')
    message = models.CharField(null=True, verbose_name='Сообщение')
    url = models.URLField(null=True, verbose_name='URL')

    target_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name='notification_target',
        blank=True,
        null=True
    )
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    objects = NotificationManager.as_manager()

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.message

    def mark_as_read(self) -> bool:
        self.is_read = True
        self.save()
        return True

@receiver(post_save, sender=Notification)
def notification_handler(**kwargs) -> None:
    """Handler to send notification"""

    instance = kwargs.pop('instance')
    if kwargs.pop('created'):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notification_{instance.to_user.username}',
            {
                'type': 'send_notification',
                'notification': {
                    'message': instance.message,
                    'created_at': instance.created_at.strftime('%Y-%m-%d %H:%m'),
                    'url': instance.url
                }
            }
        )