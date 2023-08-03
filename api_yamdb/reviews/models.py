from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель 'Категории'.

    Атрибуты:
    name -- символьное поле для хранения названия категории. -> str
    slug -- символьное поле для хранения названия-этикетки категории.
     Дефолтное значение max_length - 50 символов. -> str
    """
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель 'Жанры'.

    Атрибуты:
    name -- символьное поле для хранения названия жанра. -> str
    slug -- символьное поле для хранения названия-тикетки жанра.
     Дефолтное значение max_length - 50 символов. -> str
    """

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель 'Произведение'.

    Атрибуты:
    name -- символьное поле для хранения названия произведения. -> str
    description -- текстовое поле для идентификатора произведения. -> str
    year -- числовое поле для хранения даты издания произведения.
     Необязательное для заполнения. -> int
    genre -- ссылка на объект жанра. -> str(genre__slug)
    category -- ссылка на объект категории произведения. -> str(category_slug)
    """

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    description = models.TextField(
        verbose_name='Идентификатор произведения',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска произведения',
        blank=True,
        null=True,
        db_index=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='titles',
        verbose_name='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Вспомогательная модель для описания связи Title-Genre."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связь жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} соответствует жанрам {self.genre}'


class Review(models.Model):
    """Модель отзывов.

    Атрибуты:
    author -- ссылка на объект пользователя. -> str(user__username)
    title -- ссылка на объект произведения. -> str(title_id)
    text -- текстовое поле для храрнения текста отзыва на
     произведение. -> str
    score -- динамическое числовое поле для хранения и расчитывания среднего
     рейтинга произведения. -> int
    pub_date -- поле для хранения даты публикации отзыва.
    """

    MIN_SCORE_VALUE = 1
    MAX_SCORE_VALUE = 10

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст отзыва', )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE_VALUE),
            MaxValueValidator(MAX_SCORE_VALUE),
        ],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев.

    Атрибуты:
    author -- ссылка на объект пользователя. -> str(user__username)
    review -- ссыдка на объект отзыва. -> rewie__id
    text -- текстовое поле для храрнения текста отзыва на
     произведение. -> str
    pub_date -- поле для хранения даты публикации коментария.
     Генрируется автоматически.
    text -- текстовое поле для хранения текста комментария. -> str
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст комментария', )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.author
