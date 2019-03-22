# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import ObjectFilterQuerySetMixin
from .widgets import ObjectFilterValuesWidget


class ObjectFilterListMixin(ObjectFilterQuerySetMixin):

    def get_queryset(self):
        self.queryset = super(ObjectFilterListMixin, self).get_queryset()

        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        if hasattr(self.model, 'content_object'):
            return self.apply_user_generic_objects_filter(user=user)
        else:
            return self.apply_user_object_filter(user=user)


class _ObjectFilterDetailMixin(ObjectFilterQuerySetMixin):

    def get_object(self):
        obj = super(_ObjectFilterDetailMixin, self).get_object()

        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        self.queryset = self.model.objects.filter(id=obj.id)
        if hasattr(self.model, 'content_object'):
            if obj in self.apply_user_generic_objects_filter(user=user):
                return obj
            else:
                raise PermissionDenied
        else:
            if obj in self.apply_user_object_filter(user=user):
                return obj
            else:
                raise PermissionDenied


class ObjectFilterDetailMixin(_ObjectFilterDetailMixin):
    pass


class ObjectFilterUpdateMixin(_ObjectFilterDetailMixin):
    pass


class ObjectFilterDeleteMixin(_ObjectFilterDetailMixin):
    pass


def ObjectFilterValuesWidgetView(request, content_type_id=None, field_name=None, values=None):
    widget = ObjectFilterValuesWidget(attrs={'content_type': content_type_id,
                                             'field_name': field_name,
                                             'values': values})
    return HttpResponse(widget.render(field_name, [], ))
