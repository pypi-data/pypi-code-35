from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan, DroppedSpan


class UrllibInstrumentation(AbstractInstrumentedModule):
    name = "urllib"

    instrument_list = [
        ("urllib", "urlopen"),
        ("urllib.request", "urlopen"),
    ]

    def call(self, module, method, wrapped, instance, args, kwargs):
        url = args[0]
        signature = method.upper() + " " + url
        extra_data = {
            "wrapped_method": "Execute",
            "provider": self.name,
            "type": "Web External",
            "sub_type": "send",
            "url": url,
        }

        with CaptureSpan(signature, "ext.http.urllib", extra_data, leaf=True) as span:
            request = wrapped(*args, **kwargs)

            if not isinstance(span, DroppedSpan):
                span.context['status_code'] = request.code
                if hasattr(request, '_method'):
                    span.context['request_method'] = request._method

            return request
