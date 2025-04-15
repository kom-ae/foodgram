from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodGramUser(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    email = models.EmailField(verbose_name='email address', unique=True)
    password = models.CharField(verbose_name='пароль', max_length=128)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
