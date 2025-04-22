from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import (CreateUsersSerializer, TagSerializer,
                             UsersAvatarSerializer, UsersSerializer, IngredientSerializer)
from recipes.models import TagModel, IngredientModel

User = get_user_model()


class UsersProfileViewSet(UserViewSet):
    """Пользователь."""

    serializer_class = UsersSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUsersSerializer
        if self.action == 'me':
            return UsersSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(['put', 'delete'], detail=False, url_path='me/avatar')
    def avatar(self, request, *args, **kwargs):
        user = request.user
        if self.request.method == 'DELETE':
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = UsersAvatarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.avatar = serializer.validated_data['avatar']
            user.save()
            return Response(
                {'avatar': request.build_absolute_uri(user.avatar.url)},
                status=status.HTTP_201_CREATED
            )


class TagsViewSet(viewsets.ModelViewSet):
    """Теги."""

    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    """Ингредиенты."""

    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('get',)