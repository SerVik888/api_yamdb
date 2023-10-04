from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    confirmation_code = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
