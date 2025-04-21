from django.core.exceptions import ValidationError

from constants import MSG_AMOUNT_NULL


def validate_amount(value):
    if value == 0:
        raise ValidationError(message=MSG_AMOUNT_NULL)