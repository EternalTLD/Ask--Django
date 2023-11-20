from typing import Any

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    """Profile model"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    profile_image = models.ImageField(
        upload_to="avatars/%Y/%m/%d/", blank=True, null=True, verbose_name="Аватар"
    )
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    city = models.CharField(max_length=25, blank=True, verbose_name="Город")
    country = models.CharField(max_length=25, blank=True, verbose_name="Страна")
    status = models.CharField(max_length=250, blank=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self) -> str:
        return f"Профиль пользователя {self.user.username}"

    def get_profile_image(self) -> str:
        if self.profile_image:
            return self.profile_image.url
        return settings.MEDIA_URL + "avatars/default/avatar_default.png"

    def get_absolute_url(self) -> str:
        return reverse(
            "profiles:profile_detail", kwargs={"username": self.user.username}
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(**kwargs: Any) -> None:
    instance = kwargs.pop("instance")
    if kwargs.pop("created"):
        Profile.objects.create(user=instance)
