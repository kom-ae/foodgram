from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import render

from api.serializers import FoodgramUsersSerializer

User = get_user_model()


class FoodGramUserViewSet(UserViewSet):
    """Пользователь."""

    queryset = User.objects.all()
    serializer_class = FoodgramUsersSerializer
