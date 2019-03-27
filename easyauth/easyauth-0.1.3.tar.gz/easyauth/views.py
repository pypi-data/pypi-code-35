# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

import django_filters
import rest_framework
from django.contrib.auth import get_user_model
from django.contrib.auth import (login as django_login, logout as django_logout)
from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_framework_exception_handler

from easyauth import conf
from easyauth.permissions import DjangoModelPermissionsWithAuthenticated, IsSuperUser, IsAuthenticated,\
    PermissionViewGetPermission, GroupViewGetPermission, QueryUserModelPermission, AdminPasswordResetPermission
from easyauth.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, \
    UserPasswordResetSerializer, UserDetailSerializer, UserLogoutSerializer, AdminResetUserPasswordSerializer, \
    GroupSerializer, PermissionSerializer, UserSerializerWithDepth, GroupSerializerWithDepth

import logging


logger = logging.getLogger(__name__)


class QueryLowPermAdminModelViewSet(viewsets.ModelViewSet):
    maintain_permission_classes = (IsSuperUser, )
    query_permission_classes = (IsAuthenticated, )

    def dispatch(self, request, *args, **kwargs):
        self.is_query_permission = False
        if request.method.lower() == "get":
            self.is_query_permission = True
        return super(QueryLowPermAdminModelViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        self.permission_classes = self.maintain_permission_classes
        if hasattr(self, 'is_query_permission') and self.is_query_permission:
            self.permission_classes = self.query_permission_classes
        return super(QueryLowPermAdminModelViewSet, self).get_permissions()


class GroupViewSet(QueryLowPermAdminModelViewSet):
    query_permission_classes = (GroupViewGetPermission, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter,)
    filter_fields = ('id', 'name', )
    search_fields = ('name', )
    ordering_fields = ('id', 'name', )

    def get_serializer_class(self):
        serializer_class = GroupSerializer
        if hasattr(self, 'is_query_permission') and self.is_query_permission:
            serializer_class = GroupSerializerWithDepth

        return serializer_class


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    exclude_models = ['group', 'permission']
    permission_set_patterns = ['add_%(model_name)s', 'change_%(model_name)s', 'delete_%(model_name)s']
    exclude_permissions = []
    for m in exclude_models:
        exclude_permissions += [perm % {'model_name': m} for perm in permission_set_patterns]
    queryset = Permission.objects.exclude(codename__in=exclude_permissions)
    serializer_class = PermissionSerializer
    permission_classes = (PermissionViewGetPermission,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter,)
    filter_fields = ('id', 'codename', )
    search_fields = ('codename', 'name', )
    ordering_fields = ('id', 'codename', )


class UserViewSet(QueryLowPermAdminModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    maintain_permission_classes = (DjangoModelPermissionsWithAuthenticated,)
    query_permission_classes = (QueryUserModelPermission,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, rest_framework.filters.SearchFilter, rest_framework.filters.OrderingFilter,)

    filter_fields = ('id', get_user_model().USERNAME_FIELD, 'last_name', 'first_name', 'is_active',
                     'is_staff', 'date_joined', 'last_login', 'last_logout', 'last_login_ip')
    search_fields = (get_user_model().USERNAME_FIELD, 'last_name', 'first_name', )
    ordering_fields = ('id', get_user_model().USERNAME_FIELD, 'last_name', 'first_name', 'is_active', 'is_staff',
                       'date_joined', 'last_login', 'last_logout', 'last_login_ip')
    if get_user_model().FILTER_FIELDS:
        filter_fields += get_user_model().FILTER_FIELDS
    if get_user_model().SEARCH_FIELDS:
        search_fields += get_user_model().SEARCH_FIELDS
    if get_user_model().ORDERING_FIELDS:
        ordering_fields += get_user_model().ORDERING_FIELDS

    def create(self, request, *args, **kwargs):
        login_user = self.request.user
        __depart = self.__getDepart(login_user)
        if not login_user.is_superuser and __depart is not None:
            user_model = get_user_model()
            depart_id = __depart.id
            request.data[user_model.USER_DEPART_FIELD] = depart_id
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        login_user = self.request.user
        __depart = self.__getDepart(login_user)
        if not login_user.is_superuser and __depart is not None:
            user_model = get_user_model()
            depart_id = __depart.id
            request.data[user_model.USER_DEPART_FIELD] = depart_id
        logger.info("Update user -> %s" % json.dumps(request.data))
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        user_model = get_user_model()
        self.queryset = user_model.objects.all()
        login_user = self.request.user
        __depart = self.__getDepart(login_user)
        filter_prop = {}
        if not login_user.is_superuser:
            filter_prop['is_superuser'] = False
        if __depart is not None and __depart:
            filter_prop[user_model.USER_DEPART_FIELD] = __depart
        self.queryset = user_model.objects.filter(**filter_prop)
        return super(UserViewSet, self).get_queryset()

    def get_serializer_class(self):
        serializer_class = UserSerializer
        if hasattr(self, 'is_query_permission') and self.is_query_permission:
            serializer_class = UserSerializerWithDepth

        return serializer_class

    def __getDepart(self, user):
        user_model = get_user_model()
        if user_model.USER_DEPART_FIELD is not None and user.is_authenticated():
            return getattr(user, user_model.USER_DEPART_FIELD)
        return None


class AdminResetUsePwdView(GenericAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = AdminResetUserPasswordSerializer
    permission_classes = (AdminPasswordResetPermission,)
    __url_re = re.compile(r".*\/users\/(\d+)\/reset\/password.*")

    def put(self, request, *args, **kwargs):
        match_args = self.__url_re.search(request.path).groups()
        if len(match_args) == 1:
            self.kwargs['pk'] = long(match_args[0])
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Return the success message with OK HTTP status
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserMeView(UpdateAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = self.serializer_class(request.user).data
        return Response(data)

    def put(self, request, *args, **kwargs):
        logger.info("Self update -> %s" % json.dumps(request.data))
        self.kwargs['pk'] = request.user.id
        res = self.update(request, *args, **kwargs)
        return res

    def patch(self, request, *args, **kwargs):
        logger.info("Self partially update -> %s" % request.data)
        self.kwargs['pk'] = request.user.id
        res = self.partial_update(request, *args, **kwargs)
        return res


class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class PasswordResetView(GenericAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserPasswordResetSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.id
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the success message with OK HTTP status
        return Response(status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def login(self, request, user):
        django_login(request, user)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        logger.info("Try to login -> %s: %s" % (get_user_model().USERNAME_FIELD,
                                               request.data.get(get_user_model().USERNAME_FIELD)))
        serializer = self.get_serializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        res = self.login(request, serializer.authencated_user)
        return res


class LogoutView(GenericAPIView):
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated,)

    def logout(self, request):
        self.kwargs['pk'] = request.user.id
        django_logout(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("Logout successfully")
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def get(self, request, *args, **kwargs):
        if conf.get_conf(conf.ACCOUNT_LOGOUT_ON_GET):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)
        return self.finalize_response(request, response, *args, **kwargs)


def exception_handler(exc, context):
    if isinstance(exc, APIException):
        msg = json.dumps(exc.detail, encoding="UTF-8", ensure_ascii=False)
        logger.error("Get Error %s: %s", exc.__class__, msg)
    else:
        logger.error("Get Error %s: %s", exc.__class__, exc)
    return rest_framework_exception_handler(exc, context)
