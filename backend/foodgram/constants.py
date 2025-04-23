# Количество символов в поле slug модели Tag
TAG_SLUG_LENGTH = 32
# Количество символов в поле name модели Tag
TAG_NAME_LENGTH = 32
# Количество символов в поле name модели Ingredients
INGREDIENT_NAME_LENGTH = 128
# Количество символов в measurement_unit модели Ingredients
INGREDIENT_UNIT_LENGTH = 64
# Количество символов в name модели recipe
RECIPE_NAME_LENGTH = 256
# Количество символов в name модели ShoppingCartModel
# SHOP_CART_NAME_LENGTH = RECIPE_NAME_LENGTH

# Минимальное время приготовления
MIN_COOKING_TIME = 1
# Сообщение для непрошедшего валидацию времени приготовления
MSG_COOKING_TIME_ERROR = (
    f'Время приготовления не может быть меньше {MIN_COOKING_TIME} минуты.'
)

# Сообщение об ошибке при количестве ингредиента равном нулю
MSG_AMOUNT_NULL = 'Количество не может быть равно 0.'

# Количество слов в строке для представления объекта.
COUNT_WORD_IN_VIEW_OBJECT: int = 5
