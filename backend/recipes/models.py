import base64
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from constants import (INGREDIENT_NAME_LENGTH, INGREDIENT_UNIT_LENGTH,
                       MIN_COOKING_TIME, MSG_COOKING_TIME_ERROR,
                       RECIPE_NAME_LENGTH, SHORT_LINK_RECIPE, TAG_NAME_LENGTH,
                       TAG_SLUG_LENGTH)
from utils import get_trim_line
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
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientModel(models.Model):
    """Ингредиент."""

    name = models.CharField(
        verbose_name='Название',
        max_length=INGREDIENT_NAME_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=INGREDIENT_UNIT_LENGTH
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='Unique Ingredient-measurement_unit constraint'
            ),
        )

    def __str__(self):
        return get_trim_line(self.name)


def get_uuid():
    """Генерация коротких ссылок."""
    return base64.urlsafe_b64encode(
        uuid.uuid4().bytes
    ).replace(b'=', b'').decode()[:SHORT_LINK_RECIPE]


class RecipeModel(models.Model):
    """Рецепт."""

    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               db_index=True
                               )
    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_NAME_LENGTH,
        db_index=True
    )
    image = models.ImageField(upload_to='recipes/images/')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        IngredientModel,
        through='RecipeIngredientModel',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(TagModel, verbose_name='Тег')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message=MSG_COOKING_TIME_ERROR
            )
        ]
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата публикации.'
    )
    short_link = models.CharField(
        max_length=SHORT_LINK_RECIPE,
        unique=True,
        editable=False,
        default=get_uuid
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return '{}. Автор: {}'.format(
            get_trim_line(self.name),
            self.author.first_name
        )


class RecipeIngredientModel(models.Model):
    """Рецепт-Ингредиент."""

    recipe = models.ForeignKey(
        RecipeModel,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        IngredientModel,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[validate_amount]
    )

    class Meta:
        verbose_name = 'рецепт-ингредиент'
        verbose_name_plural = 'Рецепты-Ингредиенты'
        default_related_name = 'recipesingredients'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='Unique recipe-ingredient constraint',
            ),
        )

    def __str__(self):
        return '{} - {}'.format(
            get_trim_line(self.recipe.name),
            self.ingredient
        )
