from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import TagModel, IngredientModel

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

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar'
        )


class UsersAvatarSerializer(serializers.ModelSerializer):
    """Аватар пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta():
        model = User
        fields = (
            'avatar',
        )


class TagSerializer(serializers.ModelSerializer):
    """Тэг."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиент."""

    class Meta:
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit')
