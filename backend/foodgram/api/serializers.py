from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


User = get_user_model()


class FoodgramCreateUsersSerializer(UserCreateSerializer):
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


class FoodgramUsersSerializer(UserSerializer):
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
