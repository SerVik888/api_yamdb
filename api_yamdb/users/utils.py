import random

from django.conf import settings
from django.core.mail import send_mail


def send_code(user):
    """Cоздаём код с которым пользователь может
        войти в свою учётную записть и изменить данные.
        Отправляем этот код на указанную почту."""
    code = str(random.randint(111111, 999999))
    send_mail(
        subject='Подтверждение почты',
        message=f'Ваш код подтверждения: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    user.confirmation_code = code
