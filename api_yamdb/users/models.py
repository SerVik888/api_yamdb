from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import (
    CODE_MAX_LENGHT,
    EMAIL_MAX_LENGHT,
    NAME_MAX_LENGTH
)


class CustomUser(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
            (USER, 'пользователь'),
            (MODERATOR, 'модератор'),
            (ADMIN, 'администратор'),
    )

    username = models.CharField(
        max_length=NAME_MAX_LENGTH, unique=True,
        verbose_name='Ник-нейм пользователя',
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                'Вы не можете зарегестрировать пользователя с таким именем.'
            ),
            RegexValidator('^me$', inverse_match=True)
        ]
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGHT,
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for roles in ROLES for role in roles),
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код', max_length=CODE_MAX_LENGHT, blank=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
