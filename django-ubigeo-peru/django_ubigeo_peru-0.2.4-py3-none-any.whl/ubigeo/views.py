# -*- coding: utf-8 -*-

from django.core import serializers
from django.http import HttpResponse

from .models import Ubigeo


def region(request):
    regiones = Ubigeo.objects.filter(parent=None).order_by('name')

    if regiones:
        data = serializers.serialize("json", regiones, ensure_ascii=False)
    else:
        data = '[]'

    return HttpResponse(data, content_type='application/json')


def provincia(request):
    parent_id = request.GET.get('region_id')

    if parent_id:
        provincias = Ubigeo.objects.filter(parent=parent_id).order_by('name')
        data = serializers.serialize("json", provincias, ensure_ascii=False)
    else:
        data = '[]'

    return HttpResponse(data, content_type='application/json')


def distrito(request):
    parent_id = request.GET.get('province_id')

    if parent_id:
        distritos = Ubigeo.objects.filter(parent=parent_id).order_by('name')
        data = serializers.serialize("json", distritos, ensure_ascii=False)
    else:
        data = '[]'

    return HttpResponse(data, content_type='application/json',)
