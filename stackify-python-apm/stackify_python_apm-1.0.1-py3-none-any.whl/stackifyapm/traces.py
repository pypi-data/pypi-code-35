import json
import logging
import random
import threading
import uuid

from stackifyapm import VERSION
from stackifyapm.conf import constants
from stackifyapm.conf.constants import ASYNC_WAITING_TIME_IN_SEC
from stackifyapm.conf.constants import TRACE_CONTEXT_VERSION
from stackifyapm.utils import encoding
from stackifyapm.utils.disttracing import TraceParent, TracingOptions
from stackifyapm.utils.helper import get_current_time_in_millis


__all__ = ("CaptureSpan", "set_transaction_name", "set_transaction_result")

logger = logging.getLogger("stackifyapm.traces")
error_logger = logging.getLogger("stackifyapm.errors")

_COMPONENT_CATEGORY_MAP = {
    "database_connect": "Database",
    "database_sql": "DB Query",
    "send": "Web External",
    "cache": "Cache",
    "template": "Template",
}

_COMPONENT_DETAIL_MAP = {
    "database_connect": "Open Connection",
    "database_sql": "Execute SQL Query",
    "send": "Execute",
    "cache": "Execute",
    "template": "Template",
}

try:
    from stackifyapm.context.contextvars import get_transaction, set_transaction, get_span, set_span, clear_span  # noqa
except ImportError:
    from stackifyapm.context.threadlocal import get_transaction, set_transaction, get_span, set_span, clear_span  # noqa


class Transaction(object):
    def __init__(self, tracer, transaction_type="custom", trace_parent=None, is_sampled=True, client=None):
        """
        Create a new Transaction
        """
        self._client = client
        self._tracer = tracer

        self.id = "{:016x}".format(random.getrandbits(64))
        self.name = None
        self.transaction_type = transaction_type
        self.result = None
        self.context = {}
        self.start_time = get_current_time_in_millis()
        self.end_time = None
        self.is_sampled = is_sampled
        self.trace_parent = trace_parent

        self.exceptions = []
        self.spans = []

        self.has_async_spans = False
        self._thread_id = str(threading.current_thread().ident)

    def end_transaction(self):
        self.end_time = get_current_time_in_millis()

    def add_exception(self, exception):
        self.exceptions.append(exception)

    def begin_span(self, name, span_type, context=None, leaf=False):
        parent_span = get_span()

        if parent_span and parent_span.leaf:
            span = DroppedSpan(parent_span, leaf=True)
        else:
            span = Span(transaction=self, name=name, span_type=span_type, context=context, leaf=leaf)
            span.parent = parent_span

        if not isinstance(span, DroppedSpan):
            self.spans.append(span)

        set_span(span)
        return span

    def end_span(self):
        span = get_span()
        if span is None:
            raise LookupError()

        if isinstance(span, DroppedSpan):
            set_span(span.parent)
            return

        span.end_time = get_current_time_in_millis()

        set_span(span.parent)
        return span

    def is_done(self):
        return all([span.end_time for span in self.spans])

    def to_dict(self):
        stacks = []
        spans = [span.to_dict() for span in self.spans]
        spans.reverse()

        # convert to key-value pair for easy access
        spans_kv = {span['id']: span for span in spans}

        # arrange span and add each child to their respective parent
        for span in spans:
            if not span['parent_id'] == span['transaction_id']:
                spans_kv[span['parent_id']]['stacks'].insert(0, spans_kv.pop(span['id']))
            else:
                stacks.insert(0, spans_kv.pop(span['id']))

        result = {
            "id": self.id,
            "call": self._get_call(),
            "reqBegin": self.start_time,
            "reqEnd": self.end_time,
            "props": self._get_props(),
            "stacks": stacks,
        }
        if self.trace_parent.span_id and self.trace_parent.span_id != self.id:
            result["parent_id"] = self.trace_parent.span_id

        if self.exceptions:
            result["exceptions"] = self.exceptions

        return json.dumps(result)

    def _get_call(self):
        call = encoding.keyword_field(self.name or "").split(" ")[-1]

        if call:
            return call

        if "request" in self.context:
            return self.context["request"]["url"]["pathname"]

        return ""

    def _get_props(self):
        service_info = self._client.get_service_info()
        process_info = self._client.get_process_info()
        system_info = self._client.get_system_info()
        application_info = self._client.get_application_info()

        base_object = {
            "CATEGORY": service_info["language"]["name"].title(),
            "THREAD_ID": self._thread_id,
            "TRACETYPE": 'WEBAPP',
            "TRACE_ID": self.trace_parent.trace_id,
            "TRACE_SOURCE": "PHP",
            "TRACE_TARGET": "RETRACE",
            "TRACE_VERSION": "{}".format(VERSION or TRACE_CONTEXT_VERSION or "unknown"),
            "HOST_NAME": system_info["hostname"],
            "OS_TYPE": system_info["platform"].upper(),
            "PROCESS_ID": process_info["pid"],
            "APPLICATION_PATH": "/",
            "APPLICATION_FILESYSTEM_PATH": application_info["base_dir"],
            "APPLICATION_NAME": application_info["application_name"],
            "APPLICATION_ENV": application_info["environment"],
        }
        if "request" in self.context:
            base_object["METHOD"] = self.context["request"]["method"]
            base_object["URL"] = self.context["request"]["url"]["full"]
            base_object["REPORTING_URL"] = self.context["request"]["url"]["pathname"]

        if "response" in self.context:
            base_object["STATUS"] = self.context["response"]["status_code"]

        return base_object


class Span(object):
    __slots__ = (
        "id",
        "transaction",
        "name",
        "type",
        "context",
        "leaf",
        "parent",
        "start_time",
        "end_time",
        "is_async",
        "_thread_id",
    )

    def __init__(self, transaction, name, span_type, context=None, leaf=False, is_async=False):
        """
        Create a new Span
        """
        self.id = "{:016x}".format(random.getrandbits(64))
        self.transaction = transaction
        self.name = name
        self.type = span_type
        self.context = context
        self.leaf = leaf
        self.parent = None
        self.start_time = get_current_time_in_millis()
        self.end_time = None

        thread = threading.current_thread()
        self.is_async = True if hasattr(thread, 'transaction') else is_async
        self._thread_id = str(thread.ident)

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction.id,
            "parent_id": self.parent.id if self.parent else self.transaction.id,
            "call": encoding.keyword_field(self.type),
            "reqBegin": self.start_time,
            "reqEnd": self.end_time,
            "props": self._get_props(),
            "stacks": [],
        }

    def _get_props(self):
        base_object = {
            "CATEGORY": self._get_category(),
            "SUBCATEGORY": self._get_sub_catergory(),
        }

        if self.is_async:
            base_object["TRACETYPE"] = "ASYNC"
            base_object["THREAD_ID"] = self._thread_id

        if not self.context:
            return base_object

        if self.context.get("type", "").lower() not in ["cassandra"]:
            base_object["COMPONENT_CATEGORY"] = self._get_component_category()
            base_object["COMPONENT_DETAIL"] = self._get_component_detail()

        if self.context.get("type", "").lower() in ["database", "mongodb"] and "provider" in self.context:
            base_object["PROVIDER"] = self.context["provider"]

        if self.context.get("type", "").lower() in ["database", "cassandra"]:
            if "statement" in self.context:
                base_object["SQL"] = self.context["statement"]

        if self.context.get("type", "").lower() == "mongodb":
            if "collection" in self.context:
                base_object["MONGODB_COLLECTION"] = self.context["collection"]

        if "url" in self.context:
            base_object["URL"] = self.context["url"]

        if "status_code" in self.context:
            base_object["STATUS"] = self.context["status_code"]

        if "request_method" in self.context:
            base_object["METHOD"] = self.context["request_method"].upper()

        if "operation" in self.context:
            base_object["OPERATION"] = self.context["operation"]

        if "cache_key" in self.context:
            base_object["CACHEKEY"] = self.context["cache_key"]

        if "cache_name" in self.context:
            base_object["CACHENAME"] = self.context["cache_name"]

        if "row_count" in self.context:
            base_object["ROW_COUNT"] = self.context["row_count"]

        if self.context.get("template"):
            base_object["TEMPLATE"] = self.context["template"]

        return base_object

    def _get_category(self):
        type = encoding.keyword_field(self.type)
        return self.context and self.context.get("type", "") or type.title()

    def _get_sub_catergory(self):
        wrapped_method = self.context and self.context.get("wrapped_method")
        return wrapped_method and wrapped_method.title() or self._get_category()

    def _get_component_category(self):
        sub_type = self.context and self.context.get("sub_type", "") or ""
        return _COMPONENT_CATEGORY_MAP.get(sub_type) or self._get_category() or "Python"

    def _get_component_detail(self):
        sub_type = self.context and self.context.get("sub_type") or ""
        return _COMPONENT_DETAIL_MAP.get(sub_type) or self._get_sub_catergory() or "Other"


class DroppedSpan(object):
    __slots__ = ("leaf", "parent")

    def __init__(self, parent, leaf=False):
        self.parent = parent
        self.leaf = leaf


class Tracer(object):
    def __init__(
        self,
        queue,
        sample_rate=1.0,
        ignore_patterns=None,
    ):
        """
        Create a Tracer
        """
        self.queue = queue
        self._sample_rate = sample_rate

    def begin_transaction(self, transaction_type, trace_parent=None, client=None):
        """
        Start a new transactions and bind it in a thread-local variable
        """
        if trace_parent:
            is_sampled = bool(trace_parent.trace_options.recorded)
        else:
            is_sampled = self._sample_rate == 1.0 or self._sample_rate > random.random()

        transaction = Transaction(self, transaction_type, trace_parent=trace_parent, is_sampled=is_sampled, client=client)
        if trace_parent is None:
            transaction.trace_parent = TraceParent(
                constants.TRACE_CONTEXT_VERSION,
                str(uuid.uuid4()),
                transaction.id,
                TracingOptions(recorded=is_sampled),
            )

        set_transaction(transaction)
        return transaction

    def end_transaction(self, result=None, transaction_name=None):
        transaction = get_transaction(clear=True)
        if transaction:
            transaction.end_transaction()
            if transaction.name is None:
                transaction.name = transaction_name or ""
            if transaction.result is None:
                transaction.result = result

            if transaction.name or 'request' in transaction.context or 'response' in transaction.context:
                if transaction.has_async_spans:
                    self.queue(transaction, delay=ASYNC_WAITING_TIME_IN_SEC)
                else:
                    self.queue(transaction)
            else:
                logger.debug("Dropped transaction {}".format(transaction.id))

        return transaction

    def capture_exception(self, exception=None):
        transaction = get_transaction()

        if transaction and exception:
            transaction.add_exception(exception)

        return transaction


class CaptureSpan(object):
    def __init__(self, name=None, span_type="code.custom", extra=None, leaf=False, **kwargs):
        """
        Start a new CaptureSpan
        """
        self.name = name
        self.type = span_type
        self.extra = extra
        self.leaf = leaf

    def __enter__(self):
        transaction = get_transaction()
        if transaction and transaction.is_sampled:
            return transaction.begin_span(self.name, self.type, context=self.extra, leaf=self.leaf)

    def __exit__(self, exc_type, exc_val, exc_tb):
        transaction = get_transaction()
        if transaction and transaction.is_sampled:
            try:
                transaction.end_span()
            except LookupError:
                error_logger.info("ended non-existing span {} of type {}".format(self.name, self.type))


def set_transaction_name(name, override=True, fallback_transaction=None):
    transaction = get_transaction() or fallback_transaction
    if not transaction:
        return

    if transaction.name is None or override:
        transaction.name = name


def set_transaction_result(result, override=True, fallback_transaction=None):
    transaction = get_transaction() or fallback_transaction
    if not transaction:
        return

    if transaction.result is None or override:
        transaction.result = result


def set_transaction_context(data, key="custom", fallback_transaction=None):
    transaction = get_transaction() or fallback_transaction
    if not transaction:
        return

    if callable(data) and transaction.is_sampled:
        data = data()

    if key in transaction.context:
        transaction.context[key].update(data)
    else:
        transaction.context[key] = data
