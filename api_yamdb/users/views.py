from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAdminOrSuperuser
from users.serializers import (
    ConfirmationCodeSerializer,
    CustomUserSerializer,
    RegistrationSerializer
)
from users.utils import send_code

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает запрос на получение, создание, редактирование,
    удаления пользователя и получение пользователей."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegistrationViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Обрабатывает запрос регистрацию пользователя."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """При создании пользователя проверяем есть ли он в базе и
        если есть удаляем."""
        serializer = self.get_serializer(data=request.data)

        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).first()

        if user:
            send_code(user)
            return Response(status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmCodeTokenViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Обрабатывает запрос на получение токена."""

    serializer_class = ConfirmationCodeSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Для получения токена отравляем код который пришёл в письме если код
        совпадает с записью из базы данных, то генерируем и отправляем пароль
        иначе отпраляем ошибку."""
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if user.confirmation_code != code:
            return Response(
                'Пользователь не найден.',
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
