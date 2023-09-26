from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Genre(BaseModel):
    """Модель жанра."""
    pass


class Category(BaseModel):
    """Модель категории."""
    pass


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр',
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
