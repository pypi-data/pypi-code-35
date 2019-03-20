import requests

from djconnect.models import BaseConsumer

class SyncConsumer(BaseConsumer):
    def __init__(self, base_url, public_key, private_key):
        super(SyncConsumer, self).__init__(base_url, public_key, private_key)
        self.session = requests.session()

    def send_request(self, url, data, headers):  # pragma: no cover
        try:
            response = self.session.post(url, data=data, headers=headers)
            self.raise_for_status(response.status_code, response.content)
            return response.content
        except Exception as e:
            raise Exception("send_request error")

def provider_for_django(provider):
    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt

    def provider_view(request):
        def get_header(key, default):
            django_key = 'HTTP_%s' % key.upper().replace('-', '_')
            return request.META.get(django_key, default)
        method = request.method
        if getattr(request, 'body', None):
            signed_data = request.body
        else:
            signed_data = request.raw_post_data
        status_code, data = provider.get_response(
            method,
            signed_data,
            get_header,
        )
        return HttpResponse(data, status=status_code)
    return csrf_exempt(provider_view)

