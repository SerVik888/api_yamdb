from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class BaseListCreateDestroyView(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    """Базовый вьюсет для просмотра, создания и удаления объектов моделей."""
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
