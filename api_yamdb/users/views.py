
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает запрос на получение, создание, редактирование,
    удаления пользователя и получение пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('username',)
