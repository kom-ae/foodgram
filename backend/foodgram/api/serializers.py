from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import TagModel, IngredientModel, RecipeModel

User = get_user_model()


class CreateUsersSerializer(UserCreateSerializer):
    """Создай пользователя."""

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UsersSerializer(UserSerializer):
    """Пользователь."""

    avatar = Base64ImageField(required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.subscriber.all().filter(target_id=obj.id).exists()
        return False


class UsersAvatarSerializer(serializers.ModelSerializer):
    """Аватар пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta():
        model = User
        fields = (
            'avatar',
        )


class TagSerializer(serializers.ModelSerializer):
    """Тег."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиент."""

    class Meta:
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit')

    def to_representation(self, instance):
        return super().to_representation(instance)


class RecipeSerializer(serializers.ModelSerializer):
    """Рецепт."""

    tags = TagSerializer(many=True, read_only=True)
    author = UsersSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    # ingredients = serializers.SerializerMethodField()

    class Meta:
        model = RecipeModel
        fields = ('id', 'tags', 'author', 'ingredients')

    # def get_ingredients(self, obj):
    #     dd = IngredientSerializer(many=True, read_only=True)
    #     return True
