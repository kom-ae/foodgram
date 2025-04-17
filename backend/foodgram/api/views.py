from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import FoodgramUsersSerializer, FoodgramCreateUsersSerializer

User = get_user_model()


class FoodGramUsersViewSet(viewsets.ModelViewSet):
    """Пользователь."""

    queryset = User.objects.all()
    serializer_class = FoodgramUsersSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FoodgramCreateUsersSerializer

        return super().get_serializer_class()
