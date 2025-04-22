from django.db import models
from django.contrib.auth import get_user_model

from constants import RECIPE_NAME_LENGTH

User = get_user_model()


class ShoppingCartModel(models.Model):
    """Список покупок."""

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_NAME_LENGTH
    )
    image = models.URLField(verbose_name='Изображение')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)'
    )
