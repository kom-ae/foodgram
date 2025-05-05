from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render
from django_filters import rest_framework as filters
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.serializers import (CreateUsersSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             TagSerializer, UsersAvatarSerializer,
                             UsersSerializer)
from favorite_cart.models import FavoriteCartModel, ShoppingCartModel
from recipes.models import IngredientModel, RecipeModel, TagModel

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


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепт."""

    queryset = RecipeModel.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, ingredients=self.request.data['ingredients'])


    # def get_queryset(self):
    #     return RecipeModel.objects.all().annotate(
    #         is_favorited=Exists(
    #             FavoriteCartModel.objects.filter(
    #                 recipe=OuterRef('id'), user=self.request.user)
    #         )
    #     ).annotate(
    #         is_in_shopping_cart=Exists(
    #             ShoppingCartModel.objects.filter(
    #                 recipe=OuterRef('id'), user=self.request.user
    #             )
    #         )
    #     )
