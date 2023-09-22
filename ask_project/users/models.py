from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = models.CharField(
        max_length=25,
        unique=True,
        help_text=('Не более 25-ти символов. Буквы, цифры и @/./+/-/_ символы.'),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        },
        verbose_name='Никнейм пользователя',
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email адресом уже существует.'
        },
        verbose_name='Email',
    )
    send_messages = models.BooleanField(default=False, verbose_name='Отправлять уведомления на почту?')
    
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username