from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField


User = get_user_model()


class FoodgramCreateUsersSerializer(UserCreateSerializer):
    """Создай пользователя."""

    class Meta(UserCreateSerializer.Meta):
        model = User
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

    class Meta:
        model = User
        # ('email', 'id', 'username', 'first_name', 'last_name')
        fields = '__all__'
