# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def _create_user(self, password, is_active, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with a given email and password.
        """
        now = timezone.now()
        if not self.model.USERNAME_FIELD:
            raise ValueError('User model must have set USERNAME_FIELD')
        identifier = extra_fields.get(self.model.USERNAME_FIELD)
        if not identifier:
            raise ValueError(("User's %s must be set", self.model.USERNAME_FIELD))
        user = self.model(is_active=is_active, is_staff=is_staff, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(password, True, False, False, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        return self._create_user(password, True, True, True, **extra_fields)


_pattern = re.compile(r"^((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})")


def _phone_validator(phone):
    if not _pattern.match(phone):
        raise ValidationError(
            _('%s is a invalid phone number') % phone,
        )


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An base class implementing a fully featured User model with
    admin-compliant permissions.
    password are required. Other fields are optional.
    """
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of '
                    'deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_logout = models.DateTimeField(_('last logout'), blank=True, null=True)
    last_login_ip = models.CharField(_('last login ip'), max_length=30, blank=True)
    current_login_ip = models.CharField(_('current login ip'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    phone = models.CharField(
        _('phone'),
        max_length=100,
        unique=True,
        help_text=_('Required. cell phone number.'),
        validators=[_phone_validator],
        error_messages={
            'unique': _("The phone is already registered."),
        },
    )

    USERNAME_FIELD = "phone"

    USER_DEPART_FIELD = None
    FILTER_FIELDS = ()
    SEARCH_FIELDS = ()
    ORDERING_FIELDS = ()

    objects = UserManager()

    class Meta:
        permissions = (
            ("query_user", _("Can query user model")),
            ("query_group", _("Can query group model")),
            ("query_permission", _("Can query permission model")),
        )
        ordering = ('id',)
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def password_reset_pre_process(self, validate_data):
        pass

    def password_reset_post_process(self):
        pass

    def password_reset_password_check(self, raw_password):
        return self.check_password(raw_password)
