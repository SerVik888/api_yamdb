from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleModelFilter(FilterSet):
    """Фильтр для модели произведений."""
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        exclude = ('id', 'description')
