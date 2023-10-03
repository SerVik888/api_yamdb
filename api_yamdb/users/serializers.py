import random
from django.core.validators import RegexValidator
import re
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.response import Response

from users.models import CustomUser, User


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        # ^[\w.@+-]+\Z
        """Если кто-то пытается создать пользователя с именем 'me',
        отправляем ошибку"""
        username = data.get('username')
        # me = re.match(r'^[\w.@+-]+\Z',
        #               'username'
        #    data.get('username')
        #   )
        endpoint = self.context.get(
            'request'
        ).parser_context.get(
            'kwargs'
        ).get('username')
        if data.get('role') and endpoint == 'me':
            raise ValidationError(
                'Вы не можете менять роль пользоваетля при запросе к этому эндпоитну'
            )
        if username:
            if username == 'me' or not re.match(r'^[\w.@+-]+\Z', username):
                raise ValidationError(
                    'Вы не можете зарегестрировать пользователя с таким именем.'
                )

            # if not re.match(r'^[\w.@+-]+\Z', username):
            #     raise ValidationError(
            #         'Вы не можете.'
            #     )
        return data


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def create(self, validated_data):

        code = str(random.randint(111111, 999999))
        # code = validated_data.get('code')

        send_mail(
            subject='Подтверждение почты',
            message=f'Ваш код подтверждения: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[validated_data.get('email')]
        )
        validated_data['code'] = code
        # user, created = User.objects.get_or_create(
        #     username=validated_data.get('username'),
        #     email=validated_data.get('email')
        # )
        try:
            user, created = CustomUser.objects.get_or_create(
                username=validated_data.get('username'),
                email=validated_data.get('email')
            )
        except IntegrityError:
            # self.cleaned_data
            return Response(
                {"field_name": []},
                status=status.HTTP_400_BAD_REQUEST)

        user.confirmation_code = code
        return user

    # def update(self, instance, validated_data):
    #     instance.save()
    #     return instance

    def validate(self, data):
        """Если кто-то пытается создать пользователя с именем 'me',
        отправляем ошибку"""
        username = data.get('username')
        if username:
            if username == 'me' or not re.match(r'^[\w.@+-]+\Z', username):
                raise ValidationError(
                    'Вы не можете зарегестрировать пользователя с таким именем.'
                )
        return data


# class UserProfileSerializer(serializers.ModelSerializer):
#     role = SlugRelatedField(
#         slug_field='role', read_only=True
#     )

#     class Meta:
#         model = CustomUser
#         fields = (
#             'username', 'email', 'first_name', 'last_name', 'bio', 'role'
#         )

#     def validate(self, data):
#         # ^[\w.@+-]+\Z
#         """Если кто-то пытается создать пользователя с именем 'me',
#         отправляем ошибку"""
#         me = re.match('me')
#         if data.get('username') == 'me':
#             raise ValidationError(
#                 'Вы не можете зарегестрировать пользователя с именем `me`.'
#             )
#         return data


class ConfirmationCodeSerializer(serializers.Serializer):

    confirmation_code = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=150)
