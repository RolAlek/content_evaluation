from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя.

    Атрибуты:
    email: str: электронный адрес пользователя, обязательное поле.
    bio: str: биография пользователя.
    role: str: роль пользователя.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=ROLES,
        default='user'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self) -> str:
        return self.username
