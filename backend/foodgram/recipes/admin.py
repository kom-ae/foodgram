from django.contrib import admin

from recipes.models import TagModel, IngredientModel


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name',)


@admin.register(IngredientModel)
class IngredientModelAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('name', 'measurement_unit')
