import logging
import traceback

import wrapt

import scopeagent
from ..tracer import tags


logger = logging.getLogger(__name__)


def wrapper(wrapped, instance, args, kwargs):
    record = args[0] if len(args) >= 1 else kwargs.get('record')
    if not record.name.startswith('scopeagent'):
        logger.debug("intercepting request: instance=%s args=%s kwargs=%s", instance, args, kwargs)
        active_span = scopeagent.global_agent.tracer.active_span
        if active_span:
            kv = {
                tags.EVENT: 'log' if record.levelname != 'ERROR' else 'error',
                tags.MESSAGE: record.getMessage(),
                tags.LOG_LOGGER: record.name,
                tags.LOG_LEVEL: record.levelname,
            }
            if record.exc_info:
                etype, value, tb = record.exc_info
                if etype and value and tb:
                    kv.update({
                        tags.ERROR_KIND: etype.__name__,
                        tags.ERROR_OBJECT: ''.join(traceback.format_exception_only(etype, value)).strip(),
                        tags.STACK: ''.join(traceback.format_tb(tb)).strip(),
                    })
            if record.stack_info:
                kv.update({
                    tags.STACK: record.stack_info,
                })
            active_span.log_kv(kv, timestamp=record.created)
    return wrapped(*args, **kwargs)


def patch():
    try:
        logger.debug("patching module=logging name=StreamHandler.emit")
        wrapt.wrap_function_wrapper('logging', 'StreamHandler.emit', wrapper)
    except ImportError:
        logger.debug("module not found module=logging")
