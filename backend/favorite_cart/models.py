from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import RecipeModel

User = get_user_model()


class FavoriteCartAbstractModel(models.Model):
    """Абстрактный класс для избранного и корзины."""

    recipe = models.ForeignKey(
        RecipeModel,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='Unique recipe_user constraint, %(app_label)s_%(class)s',
            ),
        )

    def __str__(self):
        return '{}. У пользователя: {}'.format(
            self.recipe, self.user
        )


class ShoppingCartModel(FavoriteCartAbstractModel):
    """Список покупок."""

    class Meta(FavoriteCartAbstractModel.Meta):
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shoppings_carts'


class FavoriteModel(FavoriteCartAbstractModel):
    """Избранное."""

    class Meta(FavoriteCartAbstractModel.Meta):
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        default_related_name = 'favorites'
