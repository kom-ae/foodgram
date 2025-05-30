from rest_framework import serializers

from recipes.models import IngredientModel, TagModel


def validate_ingredients(value):
    if not value:
        raise serializers.ValidationError('Не определены ингредиенты.')
    ingredients_id = [item['id'] for item in value]
    if len(ingredients_id) != len(set(ingredients_id)):
        raise serializers.ValidationError('Ингредиенты повторяются.')
    if (len(ingredients_id)
            != IngredientModel.objects.filter(pk__in=ingredients_id).count()):
        raise serializers.ValidationError('Не все ингредиенты есть в базе.')
    amount_false = []
    for item in value:
        ingr_id, amount = item.values()
        if amount <= 0:
            amount_false.append(ingr_id)
    if amount_false:
        raise serializers.ValidationError(
            'Количество ингредиента {} должно быть больше 0'.format(
                (', ').join(
                    [
                        item[0] for item in
                        IngredientModel.objects.values_list('name').filter(
                            pk__in=amount_false
                        )
                    ]
                )
            )
        )
    return value


def validate_tags(value):
    if not value:
        raise serializers.ValidationError('Не определены тэги.')
    tags_id = [item.id for item in value]
    if len(tags_id) != len(set(tags_id)):
        raise serializers.ValidationError('Тэги повторяются.')
    if (len(tags_id)
            != TagModel.objects.filter(pk__in=tags_id).count()):
        raise serializers.ValidationError('Не все тэги есть в базе.')
    return value


def validate_subscribe(data):
    user = data.get('user')
    target = data.get('target')
    if user.subscriber.filter(target=target).exists():
        raise serializers.ValidationError(
            'На этого пользователя уже подписаны.'
        )
    if user == target:
        raise serializers.ValidationError(
            'Нельзя подписываться на самого себя.'
        )
    return data

# Проверка существования записи происходит на уровне модели
# в эту проверку при существующей записи выполнение не заходит
# ошибка выкидывается раньше

# def validate_favorite(data):
#     recipe = data.get('recipe')
#     user = data.get('user')
#     if user.favorites.filter(recipe=recipe).exists():
#         raise serializers.ValidationError('Рецепт уже добавлен в избранное.')
#     return data
