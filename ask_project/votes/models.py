from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VoteManager(models.Manager):
    """Vote manager"""

    def count_likes(self):
        """Returns value of object likes"""
        likes = self.get_queryset().filter(vote=1).count()
        return likes

    def count_dislikes(self):
        """Returns value of object dislikes"""
        dislikes = self.get_queryset().filter(vote=-1).count()
        return dislikes


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = ((LIKE, "like"), (DISLIKE, "dislike"))

    vote = models.SmallIntegerField(choices=VOTES, verbose_name="Голос")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="Пользователь",
    )
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Дата")

    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        related_name="vote_target"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = VoteManager()
