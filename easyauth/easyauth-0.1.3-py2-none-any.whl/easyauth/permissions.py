# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, AllowAny, DjangoModelPermissions


class AuthenticatedChecker(object):
    @staticmethod
    def is_authenticated(request):
        return request.user and (request.user.is_authenticated() if callable(request.user.is_authenticated)
                                 else request.user.is_authenticated)


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return AuthenticatedChecker.is_authenticated(request) and request.user.is_superuser


class IsStaff(BasePermission):
    """
    Allows access only to staff.
    """

    def has_permission(self, request, view):
        return AuthenticatedChecker.is_authenticated(request) and request.user.is_staff


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return AuthenticatedChecker.is_authenticated(request)


class PermissionsAll(BasePermission):
    permission_classes = (IsAuthenticated, )

    def has_permission(self, request, view):
        if not self.permission_classes:
            return True
        for permission in [permission() for permission in self.permission_classes]:
            if not permission.has_permission(request, view):
                return False
        return True


class PermissionsAny(BasePermission):
    permission_classes = (AllowAny, )

    def has_permission(self, request, view):
        if not self.permission_classes:
            return True
        for permission in [permission() for permission in self.permission_classes]:
            if permission.has_permission(request, view):
                return True
        return False


class DBBasedPermissionsAll(BasePermission):
    required_permission_names = []

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        perms = ['%s.%s' % (view.queryset.model._meta.app_label if perm != 'query_group' and perm != 'query_permission'
                            else request.user._meta.app_label, perm) for perm in self.required_permission_names]
        return request.user.has_perms(perms)


class DBBasedPermissionsAny(BasePermission):
    required_permission_names = []

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        if not self.required_permission_names:
            return True
        for item in self.required_permission_names:
            if request.user.has_perm(item):
                return True
        return False


class DjangoModelPermissionsWithAuthenticated(PermissionsAll):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)


class AdminPasswordResetPermission(PermissionsAny):
    permission_classes = (IsSuperUser, DjangoModelPermissionsWithAuthenticated)


class QueryUserModelPermission(DBBasedPermissionsAll):
    required_permission_names = ["query_user"]


class QueryGroupModelPermission(DBBasedPermissionsAll):
    required_permission_names = ["query_group"]


class QueryPermissionModelPermission(DBBasedPermissionsAll):
    required_permission_names = ["query_permission"]


class GroupViewGetPermission(PermissionsAny):
    permission_classes = (IsSuperUser, QueryGroupModelPermission)


class PermissionViewGetPermission(PermissionsAny):
    permission_classes = (IsSuperUser, QueryPermissionModelPermission)
