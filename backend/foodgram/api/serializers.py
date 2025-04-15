from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()


class FoodgramCreateUsersSerializer(UserCreateSerializer):
    """Пользователь."""

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


# class FoodgramUsersSerializer(UserSerializer):
#     """Пользователь."""

#     class Meta:
#         model = User
#         # ('email', 'id', 'username', 'first_name', 'last_name')
#         fields = '__all__'
