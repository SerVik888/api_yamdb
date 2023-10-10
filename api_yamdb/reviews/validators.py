from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверяет, что год не больше текущего."""
    if value > dt.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего'
        )
    return value
