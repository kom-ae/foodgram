from django.contrib import admin

from recipes.models import TagModel, IngredientModel, RecipeModel, RecipeIngredientModel


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('name', 'slug')
    search_fields = ('name',)


class RecipeIngredientInLine(admin.TabularInline):
    """InLine представление промежуточной модели рецептов и ингредиентов."""
    verbose_name = 'ингредиент'
    verbose_name_plural = 'Ингредиенты'
    model = RecipeIngredientModel
    extra = 0
    fields = ('recipe', 'ingredient', 'get_unit', 'amount')
    readonly_fields = ('get_unit',)

    @admin.display(description='Единицы измерения')
    def get_unit(self, obj):
                return obj.ingredient.measurement_unit

@admin.register(IngredientModel)
class IngredientModelAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    inlines = (RecipeIngredientInLine,)
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('measurement_unit',)


@admin.register(RecipeModel)
class RecipeModelAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    inlines = (RecipeIngredientInLine,)
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)


@admin.register(RecipeIngredientModel)
class RecipeIngredientModelAdmin(admin.ModelAdmin):
    """Админка рецепт - ингредиент."""

    list_display = ('recipe', 'ingredient', 'get_unit', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe',)
    fields = ('recipe', 'ingredient', 'get_unit', 'amount')
    readonly_fields = ('get_unit',)

    @admin.display(description='Единицы измерения.')
    def get_unit(self, obj):
        return obj.ingredient.measurement_unit


admin.site.empty_value_display = '-пусто-'
