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
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CreateUsersSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             TagSerializer, UsersAvatarSerializer,
                             UsersSerializer)
from favorite_cart.models import FavoriteModel, ShoppingCartModel
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
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if FavoriteModel.objects.filter(recipe=recipe, user=user).exists():
                return Response(
                    {'detail': 'Рецепт уже добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            fav_instance = user.favorites.create(recipe=recipe)
            return Response(
                {
                    'id': fav_instance.id,
                    'name': recipe.name,
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': recipe.cooking_time
                },
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            fav_instance = FavoriteModel.objects.filter(
                user=user,
                recipe=recipe
            )
            if not fav_instance:
                return Response(
                    {'detail': 'Рецепт в избранном не найден.'},
                    status=status.HTTP_400_BAD_REQUEST)
            fav_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        



# class FavoriteModelViewSet(viewsets.ModelViewSet):
#     """Избранное."""

#     queryset = FavoriteModel.objects.all()
#     permission_classes = (IsAuthenticated,)
#     # http_method_names = ['post', 'delete']

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return FavoriteSerializer
#         return FavoriteDeleteSerializer

#     def _get_recipe(self):
#         return get_object_or_404(
#             RecipeModel, pk=self.kwargs.get('recipe_id')
#         )

#     @action(methods=['DELETE'], detail=False, url_path='favorite')
#     def favorite(self, request, *args, **kwargs):
#         pass

#     # def get_object(self):
#     #     user = self.request.user
#     #     recipe = self._get_recipe()
#     #     return get_object_or_404(FavoriteModel, user=user, recipe=recipe)

#     def perform_create(self, serializer):
#         return serializer.save(
#             user=self.request.user,
#             recipe=self._get_recipe()
#         )

#     def perform_destroy(self, instance):
#         return super().perform_destroy(instance)
