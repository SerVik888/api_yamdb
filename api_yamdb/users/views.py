import random

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser, User
from users.permissions import IsUserRequest
# from users.permissions import IsMeRequest, IsUserRequest
from users.serializers import (
    ConfirmationCodeSerializer,
    CustomUserSerializer,
    RegistrationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает запрос на получение, создание, редактирование,
    удаления пользователя и получение пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsUserRequest,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    # def perform_create(self, serializer):
    #     """При регистрации пользователя передаём данные
    #     пользователя в сериалайзер"""
    #     serializer.save(user=self.request.user)

    def get_object(self):
        """Получаем объект пользователя, если отправляем запрос
        к 'users/me' по получем данные о своём прфиле."""
# TODO похоже в тесте он попадает сюда и должен вернуть 200
# TODO  а возвращает 404 потому что такого пользователя нет.
        # if self.kwargs.get('username') == 'me' and self.request.user.username:
        #     return User.objects.get(
        #         username=self.request.user.username
        #     )
        if self.kwargs.get('username') == 'me':
            return get_object_or_404(
                User, username=self.request.user.username
            )
        return get_object_or_404(User, username=self.kwargs['username'])


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # code = str(random.randint(111111, 999999))
        # request.data['code'] = code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #     try:
    #         user, created = CustomUser.objects.get_or_create(
    #             username=request.data.get('username'),
    #             email=request.data.get('email')
    # )
# TODO надо убрать error
#         except IntegrityError:
#             # self.cleaned_data
#             return Response(
#                 {"field_name": []},
#                 status=status.HTTP_400_BAD_REQUEST)

#         code = str(random.randint(111111, 999999))

#         send_mail(
#             subject='Подтверждение почты',
#             message=f'Ваш код подтверждения: {code}',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[request.data.get('email')]
#         )

#         user.confirmation_code = code


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
            user = User.objects.get(
                username=username
            )
            if user.confirmation_code != code:
                return Response(
                    'Пользователь не найден.',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            # except CustomUser.DoesNotExist as error:
            # CustomUser.DoesNotExist.error
            return Response(
                'Пользователь не найден.',
                status=status.HTTP_404_NOT_FOUND
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
