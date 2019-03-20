import logging
import traceback
from datetime import datetime
from inspect import isclass, istraceback

from ..compat import utc
from .base import Formatter


logger = logging.getLogger(__name__)


class DictFormatter(Formatter):
    @classmethod
    def dumps(cls, span):
        ret = {
            'context': {
                'trace_id': "%x" % span.context.trace_id,
                'span_id': "%x" % span.context.span_id,
                'baggage': span.context.baggage or None,
            },
            'parent_span_id': "%x" % span.parent_id if span.parent_id else None,
            'operation': span.operation_name,
            'start': (datetime.fromtimestamp(span.start_time, tz=utc)).isoformat(),
            'duration': round(span.duration * 1e9),
            'tags': span.tags or None,
            'logs': [{
                'timestamp': (datetime.fromtimestamp(log.timestamp, tz=utc)).isoformat(),
                'fields': {
                    k: cls._serialize(v) for k, v in log.key_values.items()
                }
            } for log in span.logs],
        }
        logger.debug("formatting span %s", ret)
        return ret

    @classmethod
    def _serialize(cls, value):
        if isclass(value):
            return value.__name__
        elif isinstance(value, Exception):
            return ''.join(traceback.format_exception_only(value.__class__, value)).strip()
        elif istraceback(value):
            return ''.join(traceback.format_tb(value)).strip()
        else:
            return str(value)
