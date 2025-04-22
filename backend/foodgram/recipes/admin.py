from django.contrib import admin

from recipes.models import TagModel, IngredientModel, RecipeModel, RecipeIngredientModel


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(IngredientModel)
class IngredientModelAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('measurement_unit',)


@admin.register(RecipeModel)
class RecipeModelAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = ('name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('tags',)
    filter_horizontal = ('ingredients', 'tags')
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "ingredients":
            kwargs["queryset"] = Car.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(RecipeIngredientModel)
class RecipeIngredientModelAdmin(admin.ModelAdmin):
    """Админка рецепт - ингредиент."""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe',)


admin.site.empty_value_display = '-пусто-'
