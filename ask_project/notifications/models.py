from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()

class NotificationManager(models.query.QuerySet):
    
    def recieved(self, to_user):
        qs = self.filter(to_user=to_user)
        return qs
    
    def sent(self, from_user):
        qs = self.filter(from_user=from_user)
        return qs
    
    def unread(self, to_user):
        qs = self.filter(to_user=to_user, is_read=False)
        return qs
    
    def mark_all_as_read(self, to_user):
        qs = self.unread(to_user=to_user)
        qs.update(is_read=True)
        return qs

class Notification(models.Model):
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_notifications', 
        verbose_name='Отправитель',
    )
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='recieved_notifications', 
        verbose_name='Получатель'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Отправлено')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    message = models.CharField(null=True, verbose_name='Сообщение')

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
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.message

    def mark_as_read(self):
        self.is_read = True
        self.save()
        return True