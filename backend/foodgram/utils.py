from django.utils.text import Truncator

from constants import COUNT_WORD_IN_VIEW_OBJECT


def get_trim_line(value: str) -> str:
    """Верни обрезанную строку, для текстового представления объекта.

    Параметры:
    value (str): строка для обрезки.

    Возвращаемое значение:
    Обрезанная строка.
    Количество слов в строке задается в константе COUNT_WORD_IN_VIEW_OBJECT.
    """
    return Truncator(value).words(COUNT_WORD_IN_VIEW_OBJECT)
