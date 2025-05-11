import io

from django.contrib.auth import get_user_model
from django.db.models import Exists, F, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters as rf_filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CreateUsersSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeMinifiedSerializer,
                             RecipeSerializer, SubscribedUserSerializer,
                             TagSerializer, UsersAvatarSerializer,
                             UsersSerializer)
from favorite_cart.models import FavoriteModel, ShoppingCartModel
from recipes.models import (IngredientModel, RecipeIngredientModel,
                            RecipeModel, TagModel)

User = get_user_model()


class UsersProfileViewSet(UserViewSet):
    """Пользователь."""

    serializer_class = UsersSerializer
    # pagination_class = LimitOffsetPagination

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
                status=status.HTTP_200_OK
            )

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request, *args, **kwargs):
        """Выдай все подписки пользователя."""
        user = request.user
        subscriptions = User.objects.filter(
            pk__in=user.subscriber.values_list('target', flat=True)
        )
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscribedUserSerializer(
                page,
                many=True,
                context={
                    'request': request,
                    'recipes_limit': request.query_params.get(
                        'recipes_limit'
                    )
                }
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscribedUserSerializer(
            subscriptions,
            many=True,
            context={
                'request': request,
                'recipes_limit': request.query_params.get(
                    'recipes_limit'
                )
            }
        )
        return Response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, *args, **kwargs):
        """Создай, удали подписку на пользователя."""
        user = request.user
        target = self.get_object()
        if request.method == 'POST':
            if user.subscriber.filter(target=target).exists():
                return Response(
                    {'detail': 'На этого пользователя уже подписаны.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == target:
                return Response(
                    {'detail': 'Нельзя подписываться на самого себя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.subscriber.create(target=target)
            serializer = SubscribedUserSerializer(
                target,
                context={
                    'request': request,
                    'recipes_limit': request.query_params.get(
                        'recipes_limit'
                    )
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscriber_instance = user.subscriber.filter(target=target)
            if subscriber_instance:
                subscriber_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'На этого пользователя не подписаны.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TagsViewSet(viewsets.ModelViewSet):
    """Теги."""

    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    """Ингредиенты."""

    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (AllowAny,)
    pagination_class = None
    filterset_fields = ('name',)
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
        """Добавь, удали рецепт из избранного."""
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if user.favorites.filter(recipe=recipe).exists():
                return Response(
                    {'detail': 'Рецепт уже добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            fav_instance = user.favorites.create(recipe=recipe)
            serializer = RecipeMinifiedSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            fav_instance = user.favorites.filter(recipe=recipe)
            if fav_instance:
                fav_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'Рецепт в избранном не найден.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='get-link')
    def get_link(self, request, *args, **kwargs):
        link = self.get_object().short_link
        return Response(
            {'short-link': request.build_absolute_uri('/') + 's/' + link}
        )

    @action(
        methods=['get',],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        """Файл со списком покупок."""
        user = request.user
        shopping_cart = user.shoppings_carts.values_list('recipe', flat=True)
        ingredients = RecipeIngredientModel.objects.filter(
            recipe__in=shopping_cart
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(count=Sum('amount'))
        if shopping_cart:
            buffer = io.StringIO()

            for item in ingredients:
                line = '{} ({}) - {}'.format(
                    item['ingredient__name'],
                    item['ingredient__measurement_unit'],
                    item['count']
                )
                buffer.write(line + '\n')
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="data.txt"'
            return response
        return Response(
            {'detail': 'Список покупок пуст.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, *args, **kwargs):
        """Добавить, удалить рецепт из списка покупок."""
        user = request.user
        recipe = self.get_object()
        shoppings_carts_inst = user.shoppings_carts.filter(recipe=recipe)
        if request.method == 'POST':
            if shoppings_carts_inst.exists():
                return Response(
                    {'detail': 'Рецепт уже добавлен с список покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.shoppings_carts.create(recipe=recipe)
            serializer = RecipeMinifiedSerializer(
                recipe,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if shoppings_carts_inst.exists():
                shoppings_carts_inst.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'Рецепта не было в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )


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
