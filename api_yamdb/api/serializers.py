from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        lookup_field = 'slug'
        fields = ('name', 'slug')
        model = Genre


class GETTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )

        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating)
        return None


class PostPatchTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )

        model = Title

    def get_rating(self, obj):
        """Вычисляет рейтинг произведения."""
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating)
        return None

    def to_representation(self, instance):
        """Передаёт данные в сериализатор, использующийся для чтения."""
        serializer = GETTitleSerializer(instance)
        return serializer.data

    def validate_year(self, value):
        """Проверяет, что значение года не больше текущего."""
        if value > datetime.now().year:
            raise serializers.ValidationError('Недопустимое значение.')
        return value
