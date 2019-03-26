from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.list import ListView
from . import process_webhook
from .exceptions import DoesNotExist, RequestError
from .models import Request
import json


class ReceiverView(View):
    def post(self, request, source_slug):
        try:
            response = process_webhook(source_slug, request)
        except DoesNotExist:
            return HttpResponse(
                json.dumps(
                    {
                        'status': 404,
                        'title': 'Not Found',
                        'detail': (
                            'Handler not found for \'%s\' webhook.' % source_slug
                        )
                    }
                ),
                status=404,
                content_type='application/json'
            )
        except RequestError as ex:
            return HttpResponse(
                json.dumps(
                    {
                        'status': 400,
                        'title': 'Bad Request',
                        'detail': str(ex)
                    }
                ),
                status=400,
                content_type='application/json'
            )

        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )


class RequestListView(ListView):
    model = Request

    def get_queryset(self):
        return super().get_queryset().filter(
            handler=self.kwargs['source_slug']
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            handler=self.kwargs['source_slug'],
            url=self.request.build_absolute_uri(
                reverse('webhook_receiver', kwargs=self.kwargs)
            )
        )
