from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        """Если кто-то пытается создать пользователя с именем 'me',
        отправляем ошибку"""
        if data.get('username') == 'me':
            raise ValidationError(
                'Вы не можете зарегестрировать пользователя с именем `me`.'
            )
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    role = SlugRelatedField(
        slug_field='role', read_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ConfirmationCodeSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
