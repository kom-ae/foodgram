from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodGramUser(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text='Обязательное поле.'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text='Обязательное поле.')
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        help_text='Обязательное поле.'
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        default=None
    )
    password = models.CharField(verbose_name='пароль', max_length=128)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = "email"

    class Meta(AbstractUser.Meta):
        pass
