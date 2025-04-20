from django.db import models

from constants import TAG_NAME_LENGTH, TAG_SLUG_LENGTH


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
