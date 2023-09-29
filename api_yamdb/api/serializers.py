from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, GenreTitle


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
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
        return rating

    def to_internal_value(self, data):
        fixed_data = data.copy()
        print(Category.objects.all())
        if data.get('category'):
            category = Category.objects.get(slug=data['category'])
            fixed_data['category'] = category
        if data.get('genre'):
            genre = [Genre.objects.get(slug=obj) for obj in data['genre']]
            fixed_data['genre'] = genre
        return fixed_data

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                GenreTitle.objects.create(title=title, genre=genre)
            return title

    def update(self, instance, validated_data):
        if 'genre' not in self.initial_data:
            return super().update(instance, validated_data)
        else:
            genres = validated_data.pop('genre')
            title = super().update(instance, validated_data)
            print(title.genre.all())
            title.genre.clear()
            for genre in genres:
                GenreTitle.objects.get_or_create(title=title, genre=genre)
            return title
