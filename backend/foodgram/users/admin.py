from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import FoodGramUser, SubscribeModel


@admin.register(FoodGramUser)
class FoodGramUserAdmin(UserAdmin):
    """Админка для пользователей."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'subscribe',
        'recipes',
        'is_staff'
    )
    search_fields = ('email', 'username')
    readonly_fields = ('subscribe', 'recipes')

    @admin.display(description='Подписчиков')
    def subscribe(self, obj):
        return obj.target.count()

    @admin.display(description='Рецептов')
    def recipes(self, obj):
        return obj.recipes.count()


@admin.register(SubscribeModel)
class SubscribeModelAdmin(admin.ModelAdmin):
    """Админка подписок."""

    list_display = ('user', 'target')
    search_fields = ('user__email', 'target__email')
