import random
import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()


def validate_username(data):
    """Если кто-то пытается создать пользователя с именем 'me'
    или имя не соответствует требованиям отправляем ошибку."""
    username = data.get('username')
    if username:
        if username == 'me' or not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError(
                'Вы не можете зарегестрировать пользователя с таким именем.'
            )


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        """Ещё проверяем что бы пользователь не мог поменять поле 'role'
        при запросе к 'me'"""
        endpoint = self.context.get(
            'request'
        ).parser_context.get(
            'kwargs'
        ).get('username')
        if data.get('role') and endpoint == 'me':
            raise ValidationError(
                'Вы не можете менять роль пользоваетля при запросе к '
                'этому эндпоитну'
            )
        validate_username(data)
        return data


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        """При создании пользователя создаём код с которым пользователь может
        войти в свою учётную записть и изменить данные.
        Отправляем этот код на указанную почту."""
        code = str(random.randint(111111, 999999))
        send_mail(
            subject='Подтверждение почты',
            message=f'Ваш код подтверждения: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[validated_data.get('email')]
        )
        user, created = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )

        user.confirmation_code = code
        return user

    def validate(self, data):
        validate_username(data)
        return data


class ConfirmationCodeSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
