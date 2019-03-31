# -*- coding: utf-8 -*-

from django import forms

from ubigeo.fields import UbigeoField
from .models import Incident


class IncidentForm(forms.ModelForm):

    location = UbigeoField(required=False, with_international=True)

    class Meta:
        model = Incident
        fields = "__all__"
