

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsUserRequest
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

    def get_object(self):
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
        serializer = self.get_serializer(data=request.data)
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
            user = User.objects.get(
                username=username
            )
            if user.confirmation_code != code:
                return Response(
                    'Пользователь не найден.',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                'Пользователь не найден.',
                status=status.HTTP_404_NOT_FOUND
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
