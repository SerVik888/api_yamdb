from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api_yamdb.settings import CODE_MAX_LENGHT, NAME_MAX_LENGTH

from users.utils import send_code, validate_username

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        """Ещё проверяем что бы пользователь не мог поменять поле 'role'
        при запросе к 'me'"""
        name = self.context.get(
            'request'
        ).parser_context.get(
            'kwargs'
        ).get('username')
        if data.get('role') and name == 'me':
            raise ValidationError(
                'Вы не можете менять роль пользоваетля при запросе к '
                'этому эндпоитну'
            )
        return data


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        """При создании пользователя отправляем код на почту."""
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        send_code(user)
        return user

    def validate(self, data):
        validate_username(data)
        return data


class ConfirmationCodeSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(max_length=CODE_MAX_LENGHT)
    username = serializers.CharField(max_length=NAME_MAX_LENGTH)
