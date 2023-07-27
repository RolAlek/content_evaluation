from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    """Модель 'Категории'."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        unique=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель 'Жанры'."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель 'Произведение'."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    description = models.SlugField(
        verbose_name='Идентификатор произведения',
        max_length=50
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произведения',
        blank=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория произведения'
    )
    rating = 5

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Rating(models.Model):
    pass
