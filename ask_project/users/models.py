from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model"""

    username = models.CharField(
        max_length=25,
        unique=True,
        help_text=(
            "Less then 25 characters. Only letters, digits and @/./+/-/_ symbols."
        ),
        error_messages={"unique": "This username is already used."},
    )
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "This email is already used."},
    )
    send_messages = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username
