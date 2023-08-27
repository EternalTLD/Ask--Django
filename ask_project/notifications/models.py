from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from questions.models import Question


User = get_user_model()

class NotificationManager(models.Manager):
    
    def recieved(self, to_user):
        qs = Notification.objects.filter(to_user=to_user)
        notifications = list(qs)
        return notifications
    
    def unread(self, to_user):
        qs = Notification.objects.filter(to_user=to_user, read_at=False)
        notifications = list(qs)
        return notifications
    
    def mark_all_as_read(self, to_user):
        qs = Notification.objects.unread(to_user=to_user)
        qs.update(read_at=timezone.now)
        return True

class Notification(models.Model):
    TYPES = (
        ('QL', 'Question like'),
        ('AL', 'Answer like'),
        ('AQ', 'Answer to question')
    )
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notifications', 
        verbose_name='От пользователя'
    )
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='_notifications', 
        verbose_name='К пользователю'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Отправлено')
    read_at = models.DateTimeField(default=None, verbose_name='Прочитано')
    type = models.CharField(max_length=2, choices=TYPES)

    objects = NotificationManager()

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        unique_together = ('from_user', 'to_user')

    def __str__(self) -> str:
        if self.type == 'QL':
            return f'Пользователю {self.from_user.username} понравился вопрос {self.question.pk}'
        elif self.type == 'AL':
            return f'Пользователю {self.from_user.username} понравился ответ на вопрос {self.question.pk}'
        elif self.type == 'AQ':
            return f'Пользователь {self.from_user.username} ответил на вопрос {self.question.pk}'
        
    def timesince(self):
        pass
    
    def mark_as_read(self):
        self.read_at = timezone.now
        self.save()
        return True
