from django.contrib import admin
from django.db.models import Avg

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class TitleInline(admin.StackedInline):

    model = Title
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    inlines = (TitleInline,)
    list_display = (
        'name',
        'slug'
    )


class GenreInline(admin.StackedInline):

    model = GenreTitle
    extra = 0
    fk_name = None


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'year',
        'category',
        'get_genre',
        'get_rating'
    )
    list_editable = ('category',)
    list_filter = (
        'name',
        'year',
        'category',
    )
    inlines = (GenreInline,)

    @admin.display(description='Рейтинг')
    def get_rating(self, instance):
        rating = instance.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating)
        return None

    @admin.display(description='Жанр')
    def get_genre(self, instance):
        return ', '.join([genre.name for genre in instance.genre.all()])


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug'
    )
    inlines = (GenreInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'score',
        'pub_date'
    )
    list_filter = (
        'title',
        'author',
        'score',
        'pub_date'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'review',
        'author',
        'pub_date'
    )
