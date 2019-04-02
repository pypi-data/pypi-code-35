import inspect
import logging
import traceback

import wrapt

import scopeagent
from scopeagent.tracer import tags


logger = logging.getLogger(__name__)


class TestResultProxy(wrapt.ObjectProxy):
    def __init__(self, wrapped, span):
        super(TestResultProxy, self).__init__(wrapped)
        self._span = span

    def addError(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_ERROR)
        self._span.set_tag(tags.ERROR, True)
        self._span.log_kv({
            tags.EVENT: 'error',
            tags.MESSAGE: ''.join(traceback.format_exception_only(etype, value)).strip(),
            tags.ERROR_KIND: etype.__name__,
            tags.ERROR_OBJECT: ''.join(traceback.format_exception_only(etype, value)).strip(),
            tags.STACK: ''.join(traceback.format_tb(tb)).strip(),
        })
        return self.__wrapped__.addError(test, err)

    def addFailure(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
        self._span.set_tag(tags.ERROR, True)
        self._span.log_kv({
            tags.EVENT: 'test_failure',
            tags.MESSAGE: 'Test failed',
            tags.ERROR_KIND: etype.__name__,
            tags.ERROR_OBJECT: ''.join(traceback.format_exception_only(etype, value)).strip(),
            tags.STACK: ''.join(traceback.format_tb(tb)).strip(),
        })
        return self.__wrapped__.addFailure(test, err)

    def addSuccess(self, test):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_PASS)
        return self.__wrapped__.addSuccess(test)

    def addSkip(self, test, reason):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_SKIP)
        self._span.log_kv({
            tags.EVENT: 'test_skip',
            tags.MESSAGE: reason,
        })
        return self.__wrapped__.addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        etype, value, tb = err
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_PASS)
        self._span.log_kv({
            tags.EVENT: 'expected_failure',
            tags.MESSAGE: 'Test failed as expected',
            tags.ERROR_KIND: etype.__name__,
            tags.ERROR_OBJECT: ''.join(traceback.format_exception_only(etype, value)).strip(),
            tags.STACK: ''.join(traceback.format_tb(tb)).strip(),
        })
        return self.__wrapped__.addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self._span.set_tag(tags.TEST_STATUS, tags.TEST_STATUS_FAIL)
        self._span.set_tag(tags.ERROR, True)
        self._span.log_kv({
            tags.EVENT: 'unexpected_success',
            tags.MESSAGE: 'Test passed unexpectedly',
        })
        return self.__wrapped__.addUnexpectedSuccess(test)


def wrapper(wrapped, instance, args, kwargs):
    logger.debug("intercepting test: instance=%s args=%s kwargs=%s", instance, args, kwargs)
    result = args[0] if args else kwargs['result']

    try:
        test_method = getattr(instance, instance._testMethodName)
        file = inspect.getsourcefile(test_method)[len(scopeagent.global_agent.source_root or ''):]
        file = file.lstrip('/')
        lines, first_line = inspect.getsourcelines(test_method)
        code = "%s:%d:%d" % (file, first_line, first_line+len(lines))
    except (IOError, OSError,):
        code = ""

    with scopeagent.global_agent.tracer.start_active_span(
            operation_name=instance._testMethodName,
            tags={
                tags.SPAN_KIND: tags.TEST,
                tags.TEST_FRAMEWORK: 'unittest',
                tags.TEST_SUITE: "%s.%s" % (instance.__class__.__module__, instance.__class__.__qualname__),
                tags.TEST_NAME: instance._testMethodName,
                tags.TEST_CODE: code,
            }) as scope:
        scope.span.context.baggage[tags.TRACE_KIND] = tags.TEST
        return wrapped(TestResultProxy(result, scope.span))


def patch():
    try:
        logger.debug("patching module=unittest name=TestCase")
        wrapt.wrap_function_wrapper('unittest', 'TestCase.run', wrapper)
    except ImportError:
        logger.debug("module not found module=unittest")
