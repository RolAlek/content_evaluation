from django_filters import rest_framework as filters

from reviews.models import Title


class TitleCustomFilter(filters.FilterSet):
    """
    Класс кастомизированного фильтра для организации подборки произведений по
     отдельным полям модели Title.

    Атрибуты:
    category -- филтрация произведений по их категориям - поле 'category'.
    genre -- фильтрация произведений по их жанрам - поле 'genre'.
    name -- фильтрация произведений по названиям - поле 'name'.
    year -- фильтрация произведений по году выпуска - поле 'year'.
    """

    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    year = filters.NumberFilter(
        field_name='year',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
