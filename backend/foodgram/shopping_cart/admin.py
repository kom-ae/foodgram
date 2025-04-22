from django.contrib import admin

from recipes.models import RecipeModel
from shopping_cart.models import ShoppingCartModel
from utils import get_trim_line


@admin.register(ShoppingCartModel)
class ShoppingCartModelAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('user', 'get_recipe', 'name', 'image', 'cooking_time')
    search_fields = ('user', 'name')

    def get_recipe(self, obj):
        return get_trim_line(RecipeModel.objects.get(pk=obj.id).name)
