from time import time
from os import getenv, path
from .sender import LogSenseSender
import inspect
import logging


class FluentWrapper:
    def _build_meta(self, extra_meta={}):
        return {**extra_meta, **{'app': self._app, 'type': 'metrics'}}

    def update_meta(self, extra_meta={}):
        if self._logger:
            self._logger.update_meta(self._build_meta(extra_meta))

    def __init__(self):
        self._internal_logger = logging.getLogger('logsense.fluent-wrapper')
        self._logsense_token = None
        self._logger = None
        self._app = ''

    def setup(self, app, logsense_token, verbose=False, meta={}):
        self._app = app
        self._logsense_token = logsense_token

        if self._logsense_token:
            self._internal_logger.info("Initializing LogSense metrics wrapper")
            self._logger = LogSenseSender(self._logsense_token,
                                         'metrics',
                                         verbose=verbose,
                                         meta=self._build_meta(meta))
        else:
            self._logger = None
            self._internal_logger.warning("LogSense metrics wrapper initialization skipped, "
                                         "LOGSENSE_TOKEN is not set")

    def emit(self, label: str, value: float, optional=dict()):
        if self._logger is None:
            return

        data = {**optional, **{
            label: value
        }}
        self._logger.emit(data)


fluent_wrapper = FluentWrapper()


def setup_metrics(app: str, logsense_token: str, metadata={}):
    fluent_wrapper.setup(app, logsense_token, meta=metadata)


def _fix_special_keys(key:str):
    if key == 'customer_id':
        return '_customer_id'
    else:
        return key


def measure_duration(label: str = None, extracted_params: list = None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            t0 = time()
            result = f(*args)
            t1 = time()

            if extracted_params is not None:
                f_params = inspect.signature(f).parameters
                f_params_and_values = {
                    k: args[n] if n < len(args) else v.default
                    for n, (k, v) in enumerate(f_params.items()) if k != 'kwargs'
                }
                f_params_and_values.update(kwargs)

                extra_properties = {
                    _fix_special_keys(param): f_params_and_values.get(param) for param in extracted_params
                }
            else:
                extra_properties = {}

            _label = f.__name__ + '_duration' if label is None else label
            fluent_wrapper.emit(_label, t1 - t0, extra_properties)

            return result
        return wrapped_f
    return wrap
