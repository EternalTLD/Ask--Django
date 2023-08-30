from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()

class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    )
    vote = models.SmallIntegerField(choices=VOTES, verbose_name='Голос')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        related_name='vote_target'
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()