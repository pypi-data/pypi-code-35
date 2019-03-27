# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from easyauth import conf
from django.utils.translation import ugettext_lazy as _


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializerWithDepth(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        depth = 1


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', )
        read_only_fields = ('is_superuser', 'date_joined', 'last_login', 'last_logout',
                            'current_login_ip', 'last_login_ip')
        extra_kwargs = {'date_joined': {'read_only': True},
                        'last_login': {'read_only': True}, 'last_logout': {'read_only': True},
                        'current_login_ip': {'read_only': True}, 'last_login_ip': {'read_only': True}}

    def create(self, validated_data):
        raw_password = conf.get_conf(conf.USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN)
        validated_data["password"] = make_password(raw_password)
        user = super(UserSerializer, self).create(validated_data)
        user._password = raw_password
        return user

    def update(self, instance, validated_data):
        raw_password = None
        if "password" in validated_data:
            raw_password = validated_data["password"]
            validated_data["password"] = make_password(raw_password)
        user = super(UserSerializer, self).update(instance, validated_data)
        if raw_password:
            user._password = raw_password
        return user


class UserSerializerWithDepth(UserSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('password', )
        read_only_fields = ('is_superuser', 'date_joined', 'last_login', 'last_logout',
                            'current_login_ip', 'last_login_ip')
        extra_kwargs = {'date_joined': {'read_only': True},
                        'last_login': {'read_only': True}, 'last_logout': {'read_only': True},
                        'current_login_ip': {'read_only': True}, 'last_login_ip': {'read_only': True}}
        depth = 2


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')
        read_only_fields = ('date_joined', 'last_login', 'last_logout')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        pass


class AdminResetUserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ()

    def is_valid(self, raise_exception=False):
        return True

    def save(self, **kwargs):
        if self.instance:
            user = self.instance
            user.set_password(conf.get_conf(conf.USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN))
            user.save()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserPasswordResetSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(source='password', max_length=128)

    class Meta:
        model = get_user_model()
        fields = ('password', 'new_password')

    def is_valid(self, raise_exception=False):
        err = None
        if self.instance:
            user = self.instance
            if not user.is_active:
                err = ValidationError({'detail': _('User account disabled.')})
            else:
                user.password_reset_pre_process(self.initial_data)
                password = self.initial_data.get('password')
                new_password = self.initial_data.get('new_password')
                if password and new_password:
                    if password == new_password:
                        err = ValidationError({'detail': _('The input password and new password are the same.')})
                    elif not user.password_reset_password_check(password):
                        err = exceptions.AuthenticationFailed({'detail': _('Credentials not correct.')})
                    else:
                        self.password_reset_user = user
                else:
                    err = ValidationError({'detail': _("Must provide password and  new_password.")})
        else:
            err = exceptions.AuthenticationFailed()

        if err and raise_exception:
            raise err

        return not err

    def save(self, **kwargs):
        self.password_reset_user.set_password(self.initial_data["new_password"])
        self.password_reset_user.save()
        # because password_reset_user.save() will set _password to None
        # call pass _password(raw_password) again to reset _password
        self.password_reset_user.set_password(self.initial_data["new_password"])
        self.password_reset_user.password_reset_post_process()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (get_user_model().USERNAME_FIELD, 'password')
        read_only_fields = (get_user_model().USERNAME_FIELD, 'password')

    def is_valid(self, raise_exception=False):
        err = None
        user_model = get_user_model()
        login_name = self.initial_data.get(user_model.USERNAME_FIELD)
        password = self.initial_data.get('password')
        if login_name and password:
            user = authenticate(**self.initial_data)
            if user:
                if not user.is_active:
                    err = exceptions.AuthenticationFailed({'detail': _('User account disabled.')})
                else:
                    if 'HTTP_X_FORWARDED_FOR' in self.context["request"]._request.META:
                        from_host = "%s -> %s" % (self.context["request"]._request.META['HTTP_X_FORWARDED_FOR'],
                                                  self.context["request"]._request.META['REMOTE_ADDR'])
                    else:
                        from_host = self.context["request"]._request.META['REMOTE_ADDR']
                    setattr(user, "last_login_ip", user.current_login_ip)
                    setattr(user, "current_login_ip", from_host)
                    self.authencated_user = user
                    self.authencated_user.save()
            else:
                raise exceptions.AuthenticationFailed({'detail': _('Credentials not correct.')})
        else:
            # err = ValidationError({'detail': _("Must include '%{username}s' and '%{password}s'." % ({
            #     'username': user_model.USERNAME_FIELD,
            #     'password': 'password'
            #     }))})
            err = ValidationError({'detail': _("Must provide username and password.")})

        if err and raise_exception:
            raise err

        return not err

    def save(self, **kwargs):
        pass

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ()

    def is_valid(self, raise_exception=False):
        return True

    def save(self, **kwargs):
        if self.instance:
            user = self.instance
            if not user.is_active:
                pass
            else:
                setattr(user, "last_logout", timezone.now())
                setattr(user, "last_login_ip", user.current_login_ip)
                user.save()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ('is_active', 'password')
        read_only_fields = ('is_staff', 'is_superuser', 'date_joined', 'last_login', 'last_logout',
                            'current_login_ip', 'last_login_ip', 'groups',
                            'user_permissions', model.USERNAME_FIELD,) \
            if model.USER_DEPART_FIELD is None \
            else ('is_staff', 'is_superuser', 'date_joined', 'last_login',  'last_logout',
                  'current_login_ip', 'last_login_ip', 'groups',
                  'user_permissions', model.USERNAME_FIELD,  model.USER_DEPART_FIELD)
        depth = 2

    def create(self, validated_data):
        pass
