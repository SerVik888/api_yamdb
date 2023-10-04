from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Title

from .filters import TitleModelFilter
from .mixins import BaseListCreateDestroyView
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    GETTitleSerializer,
    PostPatchTitleSerializer
)


class CategoryViewSet(BaseListCreateDestroyView):
    """Вьюсет модели категорий."""
    pagination_class = LimitOffsetPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseListCreateDestroyView):
    """Вьюсет модели жанров."""
    pagination_class = LimitOffsetPagination
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели произведений."""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleModelFilter
    http_method_names = ['delete', 'get', 'patch', 'post']
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all()

    def get_serializer_class(self):
        """Выбирает сериализатор, в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return GETTitleSerializer
        return PostPatchTitleSerializer
