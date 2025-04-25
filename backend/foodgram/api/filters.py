"""Фильтры данных."""
from django_filters import rest_framework as filters

from recipes.models import RecipeModel


class TitleFilter(filters.FilterSet):
    """Фильтр для queryset Recipes."""

    # is_favorited = filters.BooleanFilter
    # category = filters.CharFilter(
    #     field_name='category__slug',
    #     lookup_expr='exact')
    # genre = filters.CharFilter(
    #     field_name='genre__slug',
    #     lookup_expr='exact')

    # class Meta:
    #     model = RecipeModel
    #     fields = ['category', 'genre', 'year', 'name']