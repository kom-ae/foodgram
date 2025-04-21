from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from constants import TAG_NAME_LENGTH, TAG_SLUG_LENGTH, INGREDIENT_NAME_LENGTH, INGREDIENT_UNIT_LENGTH, RECIPE_NAME_LENGTH

User = get_user_model()


class TagModel(models.Model):
    """Тэг."""

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
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'


class IngredientModel(models.Model):
    """Ингедиент."""

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
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(upload_to='recipies/images/')
    tags = models.Man
