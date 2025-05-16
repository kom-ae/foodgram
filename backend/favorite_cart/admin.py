from django.contrib import admin

from favorite_cart.models import FavoriteModel, ShoppingCartModel
from recipes.models import RecipeModel


@admin.register(ShoppingCartModel, FavoriteModel)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('recipe', 'user', 'get_recipe_cooking_time')
    search_fields = ('recipe__name', 'user__username')
    readonly_fields = ('get_recipe_cooking_time',)

    @admin.display(description='Время приготовления (в минутах)')
    def get_recipe_cooking_time(self, obj):
        return RecipeModel.objects.get(pk=obj.recipe_id).cooking_time
