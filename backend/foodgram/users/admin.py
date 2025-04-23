from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import FoodGramUser, SubscribeModel


@admin.register(FoodGramUser)
class FoodGramUserAdmin(UserAdmin):
    """Админка для пользователей."""

    search_fields = ('email', 'username')

@admin.register(SubscribeModel)
class SubscribeModelAdmin(admin.ModelAdmin):
    """Админка подписок."""

    
