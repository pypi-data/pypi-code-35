# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.core.validators import ValidationError

from .widgets import UbigeoWidget
from .models import Ubigeo


class UbigeoField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        regions = Ubigeo.objects.filter(political_division=Ubigeo.REGION)
        if kwargs.get('with_international') is None:
            regions = regions.exclude(
                reniec_code__startswith='9'
            ).order_by('name', 'id')
        self.fields = (
            forms.ModelChoiceField(
                queryset=regions,
                empty_label=_("Select Department"),
                required=False),
            forms.ModelChoiceField(
                queryset=Ubigeo.objects.filter(
                    political_division=Ubigeo.PROVINCE
                    ),
                empty_label=u"",
                required=False),
            forms.ModelChoiceField(
                queryset=Ubigeo.objects.filter(
                    political_division=Ubigeo.DISTRICT
                    ),
                empty_label=u"",
                required=False,),
            )
        self.widget = UbigeoWidget(
            self.fields[0]._get_choices(),
            self.fields[1]._get_choices(),
            self.fields[2]._get_choices(),
            attrs_1=kwargs.get('attrs_1'),
            attrs_2=kwargs.get('attrs_2'),
            attrs_3=kwargs.get('attrs_3'),
            )
        super(UbigeoField, self).__init__(
            self.fields,
            self.widget,
            *args)

    def clean(self, value):
        """I know I shouldn't override this but, Fuck this shit.
        """
        if value is None:
            return None
        v1, v2, v3 = value
        if v3 not in (None, u''):
            return Ubigeo.objects.get(pk=v3)
        elif v2 not in (None, u''):
            return Ubigeo.objects.get(pk=v2)
        elif v1 not in (None, u''):
            return Ubigeo.objects.get(pk=v1)

    def compress(self, data_list):
        if data_list:
            if data_list[2]:
                return data_list[2]
            elif data_list[1]:
                return data_list[1]
            elif data_list[0]:
                return data_list[0]
        return None

    def prepare_value(self, value):
        if value is None:
            return None
        if type(value) is tuple or type(value) is list:
            r, p, d = value
        elif type(value) is int:
            u = Ubigeo.objects.get(pk=value)
            if u.political_division == Ubigeo.DISTRICT:
                r, p, d = (u.parent.parent, u.parent, u)
            elif u.political_division == Ubigeo.PROVINCE:
                r, p, d = (u.parent, u, 0)
            elif u.political_division == Ubigeo.REGION:
                r, p, d = (u, 0, 0)
            else:
                r, p, d = (0, 0, 0)
        if r:
            self.fields[1].queryset = Ubigeo.objects.filter(parent=r)
        else:
            self.fields[1].queryset = None
        if p:
            self.fields[2].queryset = Ubigeo.objects.filter(parent=p)
        else:
            self.fields[2].queryset = None
        self.widget.provincias = self.fields[1]._get_choices()
        self.widget.distritos = self.fields[2]._get_choices()
        self.widget.decompress(d)
        return value


class DepartmentField(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self.queryset = Ubigeo.objects.filter(political_division=Ubigeo.REGION)
        super(DepartmentField, self).__init__(self.queryset, *args, **kwargs)


class ProvinceField(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self.queryset = Ubigeo.objects.none()
        super(ProvinceField, self).__init__(
            queryset=self.queryset,
            *args,
            **kwargs
        )

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = Ubigeo.objects.filter(
                pk=int(value),
                political_division=Ubigeo.PROVINCE
            )
        except (Ubigeo.DoesNotExist):
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice'
            )
        return value


class DistrictField(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        self.queryset = Ubigeo.objects.none()
        super(DistrictField, self).__init__(self.queryset, *args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = Ubigeo.objects.filter(
                pk=int(value),
                political_division=Ubigeo.DISTRICT
            )
        except (Ubigeo.DoesNotExist):
            raise ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice'
            )
        return value
