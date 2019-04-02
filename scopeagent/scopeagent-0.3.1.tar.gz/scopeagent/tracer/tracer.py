import logging
from functools import wraps

import opentracing

from ..vendor.basictracer import BasicTracer, DefaultSampler
from . import tags as cs_tags


logger = logging.getLogger(__name__)


class Tracer(BasicTracer):
    def __init__(self, recorder):
        super(Tracer, self).__init__(recorder=recorder, sampler=DefaultSampler(1))
        self.register_required_propagators()

    def register_required_propagators(self):
        from ..vendor.basictracer.text_propagator import TextPropagator
        self.register_propagator(opentracing.Format.TEXT_MAP, TextPropagator())
        self.register_propagator(opentracing.Format.HTTP_HEADERS, TextPropagator())

    def is_test_request(self):
        return self.active_span.context.baggage.get(cs_tags.SPAN_KIND, None) == 'test'
