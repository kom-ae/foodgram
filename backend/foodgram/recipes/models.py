from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from constants import (INGREDIENT_NAME_LENGTH, INGREDIENT_UNIT_LENGTH,
                       MIN_COOKING_TIME, RECIPE_NAME_LENGTH, TAG_NAME_LENGTH,
                       TAG_SLUG_LENGTH, MSG_COOKING_TIME_ERROR)
from validators import validate_amount

User = get_user_model()


class TagModel(models.Model):
    """Тег."""

    name = models.CharField(
        verbose_name='Название',
        max_length=TAG_NAME_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=TAG_SLUG_LENGTH,
        unique=True,
        null=True,
        default=None
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'


class IngredientModel(models.Model):
    """Ингредиент."""

    name = models.CharField(
        verbose_name='Название',
        max_length=INGREDIENT_NAME_LENGTH
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=INGREDIENT_UNIT_LENGTH
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeModel(models.Model):
    """Рецепт."""

    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_NAME_LENGTH,
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message=MSG_COOKING_TIME_ERROR
            )
        ]
    )
    image = models.ImageField(upload_to='recipies/images/')
    tags = models.ManyToManyField(TagModel, verbose_name='Тег', blank=True)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE
                               )
    ingredients = models.ManyToManyField(
        IngredientModel,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )

    class Meta:
        verbose_name = 'ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        default_related_name = 'recipes'


class RecipeIngredient(models.Model):
    """Рецепт-Ингредиент."""

    recipe = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(IngredientModel, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[validate_amount]
    )

    class Meta:
        verbose_name = 'рецепт-ингредиент'
        verbose_name_plural = 'Рецепты-Ингредиенты'
        default_related_name = 'recipesingredients'
