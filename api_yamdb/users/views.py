import random

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.permissions import IsAdminOrSuperUser
from users.serializers import (
    ConfirmationCodeSerializer,
    CustomUserSerializer,
    RegistrationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает запрос на получение, создание, редактирование,
    удаления пользователя и получение пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrSuperUser,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_object(self):
        """Получаем объект пользователя, если отправляем запрос
        к 'users/me' по получем данные о своём прфиле."""
        if self.kwargs['username'] == 'me':
            return get_object_or_404(
                CustomUser, username=self.request.user.username
            )
        return get_object_or_404(CustomUser, username=self.kwargs['username'])


class RegistrationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """При регистрации пользователя передаём данные
        пользователя в сериалайзер"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """При регистрации отправляем письмо с кодом подтверждения
        на адрес электронной почты, который был указан в запросе."""
        try:
            user, created = CustomUser.objects.get_or_create(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except IntegrityError:
            return Response(
                {'error': 'Отстутствует обязательное поле или оно не верно!'},
                status=status.HTTP_400_BAD_REQUEST)
        code = str(random.randint(111111, 999999))

        send_mail(
            subject='Подтверждение почты',
            message=f'Ваш код подтверждения: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.data.get('email')]
        )

        user.confirmation_code = code
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmCodeTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """Для получения токена отравляем код который пришёл в письме если код
        совпадает с записью из базы данных, то генерируем и отправляем пароль
        иначе отпраляем ошибку."""
        serializer = ConfirmationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Отсутствует обязательное поле или оно не верно.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']
        try:
            user = CustomUser.objects.get(
                confirmation_code=code, username=username
            )
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
