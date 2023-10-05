from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleModelFilter
from api.mixins import BaseListCreateDestroyView
from api.permissions import AdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GETTitleSerializer,
    PostPatchTitleSerializer,
    ReviewSerializer
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(BaseListCreateDestroyView):
    """Вьюсет модели категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseListCreateDestroyView):
    """Вьюсет модели жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели произведений."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleModelFilter
    http_method_names = ['delete', 'get', 'patch', 'post']
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        """Выбирает сериализатор, в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return GETTitleSerializer
        return PostPatchTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
