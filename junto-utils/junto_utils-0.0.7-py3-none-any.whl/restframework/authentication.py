import json

from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class User:
    """
    Простая обертка над dict,
    чтобы обращаться к аттрибутам пользователя из request в привычном django-стилей:
    request.user.id или request.user.is_superuser

    Вместо использования таких конструкций:
    request.user['id']
    """
    def __init__(self, data):
        # Для привычных обращений user.pk
        data['pk'] = data['id']
        self.__dict__ = data


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    is_superuser = serializers.BooleanField()


def get_authorization_user_data(request):
    """
    Функция-помощник, чтобы корректно вытащить авторизационный заголовок из HTTP-запроса
    """
    auth = request.META.get('HTTP_USER_DATA')
    if not auth:
        return

    try:
        user_data = json.loads(auth)
    except json.JSONDecodeError:
        raise AuthenticationFailed('Заголовок "USER_DATA" должен содержать валидный json')

    serializer = UserSerializer(data=user_data)
    if not serializer.is_valid():
        raise AuthenticationFailed({
            'detail': 'Authentication failed. Wrong USER_DATA',
            'errors': serializer.errors
        })
    return serializer.validated_data


class UserDataAuthentication(BaseAuthentication):
    """
    По json-данным из заголовка USER_DATA
    """
    def authenticate(self, request):
        user_data = get_authorization_user_data(request)
        if user_data is None:
            return None
        return User(user_data), None

    def authenticate_header(self, request):
        return 'USER_DATA'
