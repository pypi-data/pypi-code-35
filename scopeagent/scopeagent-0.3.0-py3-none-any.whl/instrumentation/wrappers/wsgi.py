import logging
from functools import wraps

import opentracing
from opentracing.ext import tags

import scopeagent


logger = logging.getLogger(__name__)


def wrap_wsgi(other_wsgi):
    @wraps(other_wsgi)
    def wsgi_tracing_middleware(environ, start_response):
        logger.debug("request intercepted environ=%s", environ)
        try:
            context = scopeagent.global_agent.tracer.extract(format=opentracing.Format.HTTP_HEADERS,
                                                        carrier=extract_headers(environ))
        except opentracing.SpanContextCorruptedException:
            context = None

        with scopeagent.global_agent.tracer.start_active_span(
            child_of=context,
            operation_name="HTTP %s" % environ['REQUEST_METHOD'],
            tags={
                tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
                tags.HTTP_URL: "%(wsgi.url_scheme)s://%(HTTP_HOST)s%(RAW_URI)s%(QUERY_STRING)s" % environ,
                tags.HTTP_METHOD: environ['REQUEST_METHOD'],
                tags.PEER_ADDRESS: "%(REMOTE_ADDR)s:%(REMOTE_PORT)s" % environ,
                tags.PEER_HOST_IPV4: environ['REMOTE_ADDR'],
                tags.PEER_PORT: environ['REMOTE_PORT'],
            }
        ) as scope:
            ret = other_wsgi(environ, start_response)
            scope.span.set_tag(tags.HTTP_STATUS_CODE, ret.status_code)
            return ret
    return wsgi_tracing_middleware


def extract_headers(request):
    prefix = 'HTTP_'
    p_len = len(prefix)
    headers = {
        key[p_len:].replace('_', '-').lower():
            val for (key, val) in request.items()
        if key.startswith(prefix)
    }
    return headers
