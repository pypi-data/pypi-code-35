from django.conf import settings
from django.urls import resolve
from .models import Request


def logging_middleware(get_response):
    def middleware(request):
        resolved = resolve(request.path)
        response = get_response(request)

        if request.method not in (
            'GET',
            'POST',
            'PUT',
            'PATCH',
            'DELETE'
        ):  # pragma: no cover
            return response

        if resolved.url_name == 'webhook_receiver' and settings.WEBHOOK_LOGGING:
            req_obj = Request.objects.create(
                handler=resolved.kwargs['source_slug'],
                request_uri=request.build_absolute_uri(),
                request_method=request.method,
                request_body=(
                    request.body and request.body.decode('utf-8') or None
                ),
                response_code=response.status_code,
                response_body=(
                    response.content and response.content.decode('utf-8') or None
                )
            )

            for key, value in request.META.items():
                if key.startswith('HTTP_'):
                    req_obj.request_headers.create(
                        name=key[5:].replace('_', ' ').capitalize().replace(' ', '-'),
                        value=value
                    )

            for key, value in response.items():
                req_obj.response_headers.create(
                    name=key,
                    value=value
                )

        return response

    return middleware
