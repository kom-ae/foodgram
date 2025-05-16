from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from constants import FIRST_NAME_LENGTH, LAST_NAME_LENGTH, PASSWORD_LENGTH


class FoodGramUser(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=FIRST_NAME_LENGTH,
        help_text='Обязательное поле.'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LAST_NAME_LENGTH,
        help_text='Обязательное поле.'
    )
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        help_text='Обязательное поле.'
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        default=''
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=PASSWORD_LENGTH
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = "email"


class SubscribeModel(models.Model):
    """Подписаться."""

    user = models.ForeignKey(
        FoodGramUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    target = models.ForeignKey(
        FoodGramUser,
        verbose_name='Цель',
        on_delete=models.CASCADE,
        related_name='target'
    )

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('target')),
                name='user_and_target_different'
            ),
            models.UniqueConstraint(
                fields=('user', 'target'),
                name='Unique user-target constraint',
            ),
        )

    def clean(self):
        if self.user == self.target:
            raise ValidationError(
                {'target': 'Нельзя подписаться на себя.'}
            )
        return super().clean()
