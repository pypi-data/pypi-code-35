# -*- coding: utf-8 -*-

from django.forms import widgets
from django.db.utils import OperationalError

from .models import Ubigeo


class UbigeoWidget(widgets.MultiWidget):

    def __init__(self, regions, provinces, districts,
                 attrs_1=None, attrs_2=None, attrs_3=None, **kwargs):
        self.regions = regions
        self.provinces = provinces
        self.districts = districts
        _widgets = [widgets.Select(), widgets.Select(), widgets.Select()]
        try:
            _widgets = (
                widgets.Select(
                    choices=self.regions,
                    attrs=attrs_1,
                ),
                widgets.Select(
                    choices=Ubigeo.objects.none(),
                    attrs=attrs_2,
                ),
                widgets.Select(
                    choices=Ubigeo.objects.none(),
                    attrs=attrs_3,
                )
            )
        except OperationalError:
            pass
        super(UbigeoWidget, self).__init__(_widgets, **kwargs)

    def decompress(self, value):
        """
        From the value stored in the DB it selects the fields and the choices
        for the select widget
        """
        if value:
            if isinstance(value, Ubigeo):
                value = value.pk
            ubigeo = Ubigeo.objects.get(pk=value)

            if ubigeo.human_political_division == 'Region':
                ubigeos = Ubigeo.objects.filter(
                    parent=ubigeo,
                    political_division=Ubigeo.PROVINCE
                )
                region_choices = [(u.pk, u.name) for u in ubigeos]
                region_choices.insert(0, (u'', ''))  # Add null case
                self.widgets[1].choices = region_choices
                return ubigeo.id, None, None

            if ubigeo.human_political_division == 'Provincia':
                ubigeos = Ubigeo.objects.filter(
                    parent=ubigeo.parent,
                    political_division=Ubigeo.PROVINCE
                )
                self.widgets[1].choices = ((u.pk, u.name) for u in ubigeos)
                ubigeos = Ubigeo.objects.filter(
                    parent=ubigeo,
                    political_division=Ubigeo.DISTRICT
                )
                province_choices = [(u.pk, u.name) for u in ubigeos]
                province_choices.insert(0, (u'', ''))  # Add null case
                self.widgets[2].choices = province_choices
                return ubigeo.parent.id, ubigeo.id, None

            if ubigeo.human_political_division == 'Distrito':
                ubigeos = Ubigeo.objects.filter(
                    parent=ubigeo.parent.parent,
                    political_division=Ubigeo.PROVINCE
                )
                self.widgets[1].choices = ((u.pk, u.name) for u in ubigeos)
                ubigeos = Ubigeo.objects.filter(
                    parent=ubigeo.parent,
                    political_division=Ubigeo.DISTRICT
                )
                self.widgets[2].choices = ((u.pk, u.name) for u in ubigeos)
                return ubigeo.parent.parent.id, ubigeo.parent.id, ubigeo.id
        return None, None, None
