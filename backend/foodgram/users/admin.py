from django.contrib import admin

from users.models import FoodGramUser


@admin.register(FoodGramUser)
class FoodGramUserAdmin(admin.ModelAdmin):
    """Админка для пользователей."""
