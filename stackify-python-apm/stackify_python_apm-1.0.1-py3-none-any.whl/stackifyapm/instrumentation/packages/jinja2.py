from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import get_method_name


class Jinja2Instrumentation(AbstractInstrumentedModule):
    name = "jinja2"

    instrument_list = [("jinja2", "Template.render")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        signature = instance.name or instance.filename
        extra_data = {
            "wrapped_method": get_method_name(method),
            "provider": self.name,
            "type": "Template",
            "sub_type": "template",
        }
        with CaptureSpan(signature, "template.jinja2", extra_data):
            return wrapped(*args, **kwargs)
