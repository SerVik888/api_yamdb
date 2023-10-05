from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

current_year = dt.now().year
User = get_user_model()


class BaseModel(models.Model):
    """Базовая модель."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name[:15]

    class Meta:
        abstract = True


class Genre(BaseModel):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(
            MaxValueValidator(
                current_year,
                message='Значение года не может быть больше текущего.'
            ),

        )
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


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

    def __str__(self):
        return self.text[:15]


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

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']

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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
        default_related_name = 'comments'
