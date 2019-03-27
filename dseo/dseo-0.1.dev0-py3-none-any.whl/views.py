import magic
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import StaticData


def custom_data(request, slug):
    obj = get_object_or_404(StaticData, slug=slug)
    if obj.file:
        mime_type = magic.from_file(obj.file.path, mime=True)
        return HttpResponse(obj.file, content_type=mime_type)
    if obj.data:
        return HttpResponse(obj.data)
    raise Http404
