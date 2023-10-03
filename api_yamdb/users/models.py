from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=150, unique=True,
        verbose_name='Ник-нейм пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField(
        'Роль', choices=ROLES, default=ROLES[0][0],
    )
    confirmation_code = models.CharField('Код', max_length=6, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
