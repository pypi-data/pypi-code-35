from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ValidationErrorNotGroupedErrors(APIException):
    """
    Обходной путь для того, чтобы вызывать ValidationError в def validate(attrs)

    С ошибками формата
    {
        "key": "value"
    }

    Без преобразования в
    {
        "key": ["value"]
    }

    Для того, чтобы обойти проверку в строчке
    /rest_framework/serializers.py  439

    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)
