from django.db import models

from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='avatars/', blank=True, verbose_name='аватар')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    city = models.CharField(max_length=25, blank=True, verbose_name='Город')
    country = models.CharField(max_length=25, blank=True, verbose_name='Страна')
    status = models.CharField(max_length=250, blank=True, verbose_name='Статус')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return f'Профиль пользователя {self.user.username}'

