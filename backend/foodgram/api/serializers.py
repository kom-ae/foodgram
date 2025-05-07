from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import TagModel, IngredientModel, RecipeModel, RecipeIngredientModel
from favorite_cart.models import FavoriteModel
from api.validators import validate_ingredients as val_ingr

User = get_user_model()


class CreateUsersSerializer(UserCreateSerializer):
    """Создай пользователя."""

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UsersSerializer(UserSerializer):
    """Пользователь."""

    avatar = Base64ImageField(required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.subscriber.all().filter(target_id=obj.id).exists()
        return False


class UsersAvatarSerializer(serializers.ModelSerializer):
    """Аватар пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta():
        model = User
        fields = (
            'avatar',
        )


class TagSerializer(serializers.ModelSerializer):
    """Тег."""

    class Meta:
        model = TagModel
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиент."""

    class Meta:
        model = IngredientModel
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipe(serializers.HyperlinkedModelSerializer):
    """Ингредиенты в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientModel
        fields = ('id', 'name', 'measurement_unit', 'amount')


# class FavoriteSerializer(serializers.ModelSerializer):
#     """Избранное."""

#     name = serializers.ReadOnlyField(source='recipe.name')
#     image = serializers.SerializerMethodField()
#     cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

#     class Meta:
#         model = FavoriteModel
#         fields = ('id', 'name', 'image', 'cooking_time')

#     def get_image(self, obj):
#         return self.context['request'].build_absolute_uri(obj.recipe.image.url)

#     def validate(self, attrs):
#         recipec_id = self.context['view'].kwargs.get('recipe_id')
#         user = self.context['request'].user
#         if FavoriteModel.objects.filter(recipe=recipec_id, user=user).exists():
#             raise serializers.ValidationError(
#                 'Рецепт уже добавлен в избранное.'
#             )
#         return attrs


class RecipeSerializer(serializers.ModelSerializer):
    """Рецепт."""

    ingredients = IngredientInRecipe(source='recipesingredients', many=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UsersSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, use_url=True)


    class Meta:
        model = RecipeModel
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def _get_exists(self, reverse_link) -> bool:
        user = self.context['request'].user
        if user.is_authenticated:
            return reverse_link.all().filter(user_id=user.id).exists()
        return False

    def get_is_favorited(self, obj):
        return self._get_exists(obj.favorites)

    def get_is_in_shopping_cart(self, obj):
        return self._get_exists(obj.shoppings_carts)


class Ingredients(serializers.Serializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создай рецепт."""

    image = Base64ImageField(required=True, use_url=True)
    ingredients = Ingredients(many=True)

    class Meta:
        model = RecipeModel
        fields = (
            'ingredients',
            'tags',
            'name',
            'text',
            'cooking_time',
            'image'
        )
        read_only_fields = ('author',)

    def validate_ingredients(self, value):
        return val_ingr(value)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = RecipeModel.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredientModel.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_current = instance.recipesingredients.all()
        ingredients = validated_data.get('ingredients', [])
        ingredients_id = [item['id'] for item in ingredients]
        for ingredient in ingredients_current:
            if ingredient.ingredient_id not in ingredients_id:
                RecipeIngredientModel.objects.get(pk=ingredient.id).delete()
        for ingredient in ingredients:
            RecipeIngredientModel.objects.filter().update_or_create(
                defaults={
                    'amount': ingredient['amount']
                },
                recipe=instance,
                ingredient_id=ingredient['id'],

            )
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(validated_data.get('tags', instance.tags))
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context['request']}
        ).data
