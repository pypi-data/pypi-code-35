from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Проверяет, что в request.user сохранен идентификатор пользователя,
    тем самым разрешая доступ только авторизованным пользователям
    """
    def has_permission(self, request, view):
        return bool(request.user) and not isinstance(request.user, AnonymousUser)


class IsSuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
