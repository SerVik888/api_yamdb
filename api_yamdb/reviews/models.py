from datetime import datetime as dt

from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def validate_year(value):
    """Проверяет, что год не больше текущего."""
    if value > dt.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего'
        )
    return value


class NameSlugBaseModel(models.Model):
    """Базовая модель."""

    name = models.CharField(
        max_length=settings.GENRE_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[settings.STR_SLICE]


class Genre(NameSlugBaseModel):
    """Модель жанра."""

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlugBaseModel):
    """Модель категории."""

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=settings.TITLE_NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name[settings.STR_SLICE]


class GenreTitle(models.Model):

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Связанный жанр/произведение'
        verbose_name_plural = 'Связанные жанры/произведения'

    def __str__(self):
        return f'#{self.id}'


class BaseReviewComment(models.Model):
    """Базовая модель для отзыва и комментария."""

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст отзыва/комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации отзыва/комментария'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[settings.STR_SLICE]


class Review(BaseReviewComment):
    """Модель отзыва"""

    RATING_CHOICES = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ]
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Рейтинг',
        help_text='Рейтинг произведения'
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name="unique_title_author_pair"
            )
        ]


class Comment(BaseReviewComment):
    """Модель комментария"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(BaseReviewComment.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
