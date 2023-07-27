from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
    ('superuser', 'Суперюзер'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя.

    Атрибуты:
    email: str: электронный адрес пользователя, обязательное поле.
    bio: str: биография пользователя.
    role: str: роль пользователя.
    """

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=16, choices=ROLES, default='user')

    def __str__(self) -> str:
        return self.username
