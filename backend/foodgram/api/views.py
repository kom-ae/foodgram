from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import FoodgramUsersSerializer

User = get_user_model()


class FoodGramUsersViewSet(viewsets.ModelViewSet):
    """Пользователь."""

    queryset = User.objects.all()
    serializer_class = FoodgramUsersSerializer
