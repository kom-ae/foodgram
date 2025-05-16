"""Фильтры данных."""
from django_filters import rest_framework as filters

from recipes.models import IngredientModel, RecipeModel


class RecipeFilter(filters.FilterSet):
    """Фильтр для queryset Recipes."""

    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.CharFilter(method='filter_tags')

    class Meta:
        model = RecipeModel
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__slug__in=self.request.GET.getlist('tags'))

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(favorites__user=user)
            return queryset.exclude(favorites__user=user)
        return queryset.none() if value else queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(shoppings_carts__user=user)
            return queryset.exclude(shoppings_carts__user=user)
        return queryset.none() if value else queryset


class IngredientFilter(filters.FilterSet):
    """Фильтрация ингредиентов."""

    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = IngredientModel
        fields = ('name',)
