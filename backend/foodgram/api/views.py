from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
# from rest_framework.permissions import adm

from api.serializers import FoodgramUsersSerializer, FoodgramCreateUsersSerializer, FoodgramUsersAvatarSerializer

User = get_user_model()


class FoodGramUsersViewSet(viewsets.ModelViewSet):
    """Пользователь."""

    queryset = User.objects.all()
    serializer_class = FoodgramUsersSerializer

    def get_queryset(self):
        if self.action == 'put':
            return User.objects.all().filter(pk=self.request.user.id)
        
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create':
            return FoodgramCreateUsersSerializer
        if self.action == 'put':
            return FoodgramUsersAvatarSerializer
        return super().get_serializer_class()
