from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя.

    Атрибуты:
    email -- символьное поле для хранения адреса электронной почты
     пользователя. Уникальное значение. -> str
    bio -- текстовое поле для хранения биографии пользователя.
     Необязательное значение. -> str
    role -- символьное поле для хранения ролей пользователя.
     Значение по умалчанию == 'user'. -> str
    """

    SIMPLE_USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (SIMPLE_USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

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
        max_length=50,
        choices=ROLES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.SIMPLE_USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self) -> str:
        return self.username
