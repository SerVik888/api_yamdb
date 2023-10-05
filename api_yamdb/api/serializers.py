from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug')
        model = Genre


class GETTitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений, обрабатывающий запросы на чтение."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(required=False, default=None)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )

        model = Title


class PostPatchTitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )

        model = Title

    def to_representation(self, instance):
        """Передаёт данные в сериализатор, использующийся для чтения."""
        serializer = GETTitleSerializer(instance)
        return serializer.data

    def validate_year(self, value):
        """Проверяет, что значение года не больше текущего."""
        if value > datetime.now().year:
            raise serializers.ValidationError('Недопустимое значение.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Отзыв на данное произведение уже есть.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
