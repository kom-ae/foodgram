from django.contrib import admin

from recipes.models import RecipeModel
from favorite_cart.models import ShoppingCartModel, FavoriteCartModel


@admin.register(ShoppingCartModel, FavoriteCartModel)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('recipe', 'user', 'get_recipe_cooking_time')
    search_fields = ('recipe__name', 'user__username')
    readonly_fields = ('get_recipe_cooking_time',)

    @admin.display(description='Время приготовления (в минутах)')
    def get_recipe_cooking_time(self, obj):
        return RecipeModel.objects.get(pk=obj.recipe_id).cooking_time
