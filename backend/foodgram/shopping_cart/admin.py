from django.contrib import admin

from recipes.models import RecipeModel
from shopping_cart.models import ShoppingCartModel
from utils import get_trim_line


@admin.register(ShoppingCartModel)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('recipe', 'user', 'get_recipe_cooking_time')
    search_fields = ('user', 'name')
    fields = ('recipe', 'user', 'get_recipe_cooking_time')
    readonly_fields = ('get_recipe_cooking_time',)

    def get_recipe_name(self, obj):
        return get_trim_line(RecipeModel.objects.get(pk=obj.recipe_id).name)

    @admin.display(description='Время приготовления (в минутах)')
    def get_recipe_cooking_time(self, obj):
        return RecipeModel.objects.get(pk=obj.recipe_id).cooking_time
