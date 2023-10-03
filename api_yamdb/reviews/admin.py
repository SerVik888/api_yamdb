from django.contrib import admin
from django.db.models import Avg

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


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


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'get_rating'
    )
    list_filter = (
        'name',
        'year',
        'category',
    )
    inlines = (GenreInline,)

    def get_rating(self, instance):
        rating = instance.reviews.aggregate(Avg('score'))['score__avg']
        if rating:
            return round(rating)
        return None
    get_rating.short_description = 'Рейтинг'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    inlines = (GenreInline,)


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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'pub_date'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
