from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.validators import validate_ingredients as val_ingr
from api.validators import validate_subscribe, validate_tags
from favorite_cart.models import FavoriteModel, ShoppingCartModel
from recipes.models import (IngredientModel, RecipeIngredientModel,
                            RecipeModel, TagModel)
from users.models import SubscribeModel

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
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.subscriber.all().filter(target_id=obj.id).exists()
        return False


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Уточненный рецепт."""
    image = Base64ImageField()

    class Meta:
        model = RecipeModel
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Избранное."""

    class Meta:
        model = FavoriteModel
        fields = ('user', 'recipe')

    # Проверка существования записи происходит на уровне модели
    # в эту проверку при существующей записи выполнение не заходит
    # ошибка выкидывается раньше

    # def validate(self, attrs):
    #     return validate_favorite(attrs)

    def to_representation(self, instance):
        return RecipeMinifiedSerializer(
            instance.recipe,
            context=self.context
        ).data


class ShoppingCartSerializer(FavoriteSerializer):
    """Список покупок."""

    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCartModel


class SubscribedUserSerializer(UsersSerializer):
    """Верни данные пользователя (на которого подписан) с его рецептами."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UsersSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit'
        )
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeMinifiedSerializer(
            recipes,
            context=self.context,
            many=True
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    """Подписки."""

    class Meta:
        model = SubscribeModel
        fields = ('user', 'target')

    def validate(self, data):
        return validate_subscribe(data)

    def to_representation(self, instance):
        return SubscribedUserSerializer(
            instance.target,
            context={'request': self.context['request']}
        ).data


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
    """Создай, обнови рецепт."""

    image = Base64ImageField(required=True, use_url=True)
    ingredients = Ingredients(required=True, many=True)

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

    # в запросе передается ключ, проверил, ошибок не возникает
    def validate_ingredients(self, value):
        return val_ingr(value)

    # в запросе передается ключ, проверил, ошибок не возникает
    def validate_tags(self, value):
        return validate_tags(value)

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError('Не передана картинка рецепта.')
        return value

    def validate(self, data):
        if not data.get('tags') or not data.get('ingredients'):
            raise serializers.ValidationError('Переданы не все данные.')
        return data

    @staticmethod
    def recipe_ingredient_update_or_create(recipe, ingredients):
        for ingredient in ingredients:
            RecipeIngredientModel.objects.update_or_create(
                defaults={
                    'amount': ingredient['amount']
                },
                recipe=recipe,
                ingredient_id=ingredient['id'],
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = RecipeModel.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.recipe_ingredient_update_or_create(
            recipe=recipe,
            ingredients=ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients_current = instance.recipesingredients.all()
        ingredients = validated_data.get('ingredients', [])
        ingredients_id = [item['id'] for item in ingredients]
        for ingredient in ingredients_current:
            if ingredient.ingredient_id not in ingredients_id:
                RecipeIngredientModel.objects.get(pk=ingredient.id).delete()
        self.recipe_ingredient_update_or_create(
            recipe=instance,
            ingredients=ingredients
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
        # через super ругается что не поддерживает вложенные поля
        # return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context['request']}
        ).data
