from django.db import models
from django.contrib.auth import get_user_model

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


class FavoriteCartModel(FavoriteCartAbstractModel):
    """Избранное."""

    class Meta(FavoriteCartAbstractModel.Meta):
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


# class ShoppingCartModel(models.Model):
#     """Список покупок."""

#     recipe = models.ForeignKey(
#         RecipeModel,
#         verbose_name='Рецепт',
#         on_delete=models.CASCADE
#     )
#     user = models.ForeignKey(
#         User,
#         verbose_name='Пользователь',
#         on_delete=models.CASCADE
#     )
#     # name = models.CharField(
#     #     verbose_name='Название',
#     #     max_length=SHOP_CART_NAME_LENGTH
#     # )
#     # image = models.URLField(verbose_name='Изображение')
#     # cooking_time = models.PositiveSmallIntegerField(
#     #     verbose_name='Время приготовления (в минутах)'
#     # )

#     class Meta:
#         verbose_name = 'список покупок'
#         verbose_name_plural = 'Списки покупок'
#         default_related_name = 'shopping_cart'
#         constraints = (
#             models.UniqueConstraint(
#                 fields=('recipe', 'user'),
#                 name='Unique ShoppingCart constraint',
#             ),
#         )

#     def __str__(self):
#         return '{}. У пользователя: {}'.format(
#             self.recipe, self.user
#         )
