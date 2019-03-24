# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django_datetime_elapsed_field import DateTimeElapsedField
from django.db import models
from django_class.models import AbsClass
from django.utils.translation import gettext_lazy as _
import public


@public.add
class Category(AbsClass):
    """fields: `name`, `disabled`, `parent` (optional). methods: `getclass()`"""

    class Meta:
        app_label = 'task'

    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    disabled = models.BooleanField(_('Disabled'), default=False)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    @property
    def tasks(self):
        return self.task_set.all()


@public.add
class Task(AbsClass):
    """fields: `module_name`, `class_name`, `name`, `todo`, `disabled`, `completed_at`, `reminded_at`, `category` (optional). methods: `getclass()`"""

    class Meta:
        app_label = 'task'
        ordering = ['-created_at', 'name']

    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    disabled = models.BooleanField(_('Disabled'), default=False)
    todo = models.BooleanField(_('TODO'), null=True, blank=True, default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Category'))
    description = models.TextField(_('Description'), null=True, blank=True)

    created_at = DateTimeElapsedField(auto_now_add=True, editable=False)
    updated_at = DateTimeElapsedField(null=True, blank=True, editable=False)
    completed_at = DateTimeElapsedField(null=True, blank=True, editable=False)
    reminded_at = DateTimeElapsedField(null=True, blank=True, editable=False)

    def __str__(self):
        completed_at = None
        if self.completed_at:
            completed_at = self.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        string = '<Task id={id} name="{name}" todo={todo} module_name="{module_name}" class_name="{class_name}">'
        return string.format(
            id=self.id,
            name=self.name,
            todo=self.todo,
            module_name=self.module_name,
            class_name=self.class_name,
            completed_at=completed_at
        )

    def __repr__(self):
        return self.__str__()
