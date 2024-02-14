from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VoteManager(models.Manager):
    """Vote manager"""

    def count_likes(self):
        """Returns value of object likes"""
        likes = (
            self.get_queryset()
            .filter(vote=1)
            .aggregate(models.Count("id"))["id__count"]
            or 0
        )
        return likes

    def count_dislikes(self):
        """Returns value of object dislikes"""
        dislikes = (
            self.get_queryset()
            .filter(vote=-1)
            .aggregate(models.Count("id"))["id__count"]
            or 0
        )
        return dislikes

    def has_user_voted(self, user):
        """Check if the user has voted for the object"""
        return self.get_queryset().filter(user=user).exists()


class Vote(models.Model):
    """Vote model for likes and dislikes"""

    LIKE = 1
    DISLIKE = -1
    VOTES = ((LIKE, "like"), (DISLIKE, "dislike"))

    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    timestamp = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="vote_target"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = VoteManager()
