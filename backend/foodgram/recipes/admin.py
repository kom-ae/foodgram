from django.contrib import admin

from recipes.models import TagModel


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    """Админка тэгов."""

    list_display = ('name', 'slug')
