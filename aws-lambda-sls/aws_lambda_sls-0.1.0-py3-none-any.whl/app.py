# -*- coding: utf-8 -*-
"""
lambda sls app
"""
import os
import re
import sys
import json
import pkgutil
import decimal
import logging
import traceback
from aws_lambda_sls import signals
from aws_lambda_sls.constants import *
import types
import errno
import functools

_PARAMS = re.compile(r'{\w+}')


class ImportStringError(ImportError):
    import_name = None
    exception = None

    def __init__(self, import_name, exception):
        self.import_name = import_name
        self.exception = exception
        msg = (
            'import_string() failed for %r. Possible reasons are:\n\n'
            '- missing __init__.py in a package;\n'
            '- package or module path not included in sys.path;\n'
            '- duplicated package or module name taking precedence in '
            'sys.path;\n'
            '- missing module, class, function or variable;\n\n'
            'Debugged import:\n\n%s\n\n'
            'Original exception:\n\n%s: %s')
        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (import_name, '\n'.join(track),
                             exception.__class__.__name__, str(exception))
                break
        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.import_name,
                                 self.exception)


def import_string(import_name, silent=False):
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]
        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            module = import_string(module_name)
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)
    except ImportError as ex:
        if not silent:
            raise(
                ImportStringError,
                ImportStringError(import_name, ex),
                sys.exc_info()[2])


class Config(dict):
    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_env(self, variable_name, silent=False):
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)
        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (
                errno.ENOENT, errno.EISDIR, errno.ENOTDIR
            ):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        if isinstance(obj, dict):
            self.update(obj)
        else:
            for key in dir(obj):
                if key.isupper():
                    self[key] = getattr(obj, key)

    def from_json(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename) as json_file:
                obj = json.loads(json_file.read())
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def from_mapping(self, *mapping, **kwargs):
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))


class LambdaFunction:
    def __init__(self, func, name=None, **config):
        self.func = func
        self.name = name
        self.handler = "app.%s" % func.__name__
        self.config = config
        if not self.name:
            self.name = func.__name__

    def __call__(self, event, context):
        return self.func(event, context)


class RouteEntry(object):

    def __init__(self, view_function, view_name, path, method,
                 api_key_required=None, content_types=None):
        self.view_function = view_function
        self.view_name = view_name
        self.uri_pattern = path
        self.method = method
        self.api_key_required = api_key_required
        self.view_args = self._parse_view_args()
        self.content_types = content_types

    def _parse_view_args(self):
        if '{' not in self.uri_pattern:
            return []
        results = [r[1:-1] for r in _PARAMS.findall(self.uri_pattern)]
        return results

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Response(object):
    def __init__(self, body, headers=None, status_code=200):
        self.body = body
        if headers is None:
            headers = {}
        self.headers = headers
        self.status_code = status_code

    @staticmethod
    def handle_decimals(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return obj

    def to_dict(self):
        body = self.body
        if not isinstance(body, (str, bytes)):
            body = json.dumps(body, default=self.handle_decimals)
        response = {
            'headers': self.headers,
            'statusCode': self.status_code,
            'body': body
        }
        return response


def error_response(message, error_code, http_status_code, headers=None):
    body = {'Code': error_code, 'Message': message}
    response = Response(body=body, status_code=http_status_code,
                        headers=headers)

    return response.to_dict()


class LambdaHandleError(Exception):
    STATUS_CODE = 403

    def __init__(self, msg=''):
        super(LambdaHandleError, self).__init__(
            self.__class__.__name__ + ': %s' % msg)


class LambdaSls(object):
    decorators = []
    config_class = Config
    default_config = dict({
        'ENV': None,
        'DEBUG': None,
        'LAMBDA_TIMEOUT': DEFAULT_LAMBDA_TIMEOUT,
        'LAMBDA_MEMORY_SIZE': DEFAULT_LAMBDA_MEMORY_SIZE,
        'LAMBDA_SECURITY_GROUP_IDS': [],
        'LAMBDA_SUBNET_IDS': [],
        "LAMBDA_RUN_TIME": DEFAULT_LAMBDA_RUN_TIME,
        "LAMBDA_ROLE": None,
        "AWS_S3_BUCKET": DEFAULT_AWS_S3_BUCKET,
        "AWS_CONNECTION_TIMEOUT": DEFAULT_AWS_CONNECTION_TIMEOUT,
        "AWS_READ_TIMEOUT": DEFAULT_AWS_READ_TIMEOUT,
        "AWS_MAX_RETRY": DEFAULT_AWS_MAX_RETRY,
        "REQUIRE_PYTHON_VERSION": REQUIRE_PYTHON_VERSION,
        "PACKAGE_INCLUDE_SYS_PATH": [],
        "PACKAGE_INCLUDE_IGNORE_FILE": [],
    })
    _DEFAULT_BINARY_TYPES = [
        'application/octet-stream', 'application/x-tar', 'application/zip',
        'audio/basic', 'audio/ogg', 'audio/mp4', 'audio/mpeg', 'audio/wav',
        'audio/webm', 'image/png', 'image/jpg', 'image/jpeg', 'image/gif',
        'video/ogg', 'video/mpeg', 'video/webm',
    ]

    __pre_lambda_functions__ = {}

    def __init__(self, app_name, root_path=None, dist_path="dist", config_object=None, include=None):
        self.app_name = app_name
        self.root_path = root_path
        if not self.root_path:
            self.root_path = self.get_root_path()
        self.routes = dict()
        self.dist_path = dist_path
        self._config_source = None
        self._includes = include or []
        self._pure_lambda_functions = {}
        self.index_lambda_function = None
        self.config = self.make_config()
        if config_object:
            self.config_from_object(config_object)
        self.binary_types = list(self._DEFAULT_BINARY_TYPES)
        self.logger = logging.getLogger(self.app_name)
        self.register_decorator(self.internal_decorator)
        self.include(self._includes)
        self.init_pre_lambda_functions()

    def register_decorator(self, decorator):
        self.decorators.append(decorator)

    def init_pre_lambda_functions(self):
        for lambda_func in self.__pre_lambda_functions__.values():
            self.register_pure_lambda_function(lambda_func)

    def internal_decorator(self, func):
        @functools.wraps(func)
        def wrapper(event, context):
            if context.__class__.__name__ != "LambdaContext":
                raise TypeError("context must be LambdaContext object!")
            self.logger.info(
                "[%s-%s] lambda event: %s",
                func.name,
                context.aws_request_id,
                event
            )
            self.logger.info(
                "[%s-%s] lambda context: %s",
                func.name, context.aws_request_id, {
                    "custom": getattr(context.client_context, "custom", {}),
                    "env": getattr(context.client_context, "env", {}),
                }
            )
            try:
                ret = func(event, context)
                self.logger.info(
                    "[%s-%s] lambda result: %s",
                    func.name, context.aws_request_id, ret
                )
            except Exception as ex:
                self.logger.error(str(ex))
                self.logger.error(traceback.format_exc())
                raise ex
            return ret
        return wrapper

    def get_root_path(self):
        """Returns the path to a package or cwd if that cannot be found.  This
        returns the path of a package or the folder that contains a module.

        Not to be confused with the package path returned by :func:`find_package`.
        """
        # Module already imported and has a file attribute.  Use that first.
        mod = sys.modules.get(self.app_name)
        if mod is not None and hasattr(mod, '__file__'):
            return os.path.dirname(os.path.abspath(mod.__file__))

        loader = pkgutil.get_loader(self.app_name)
        if loader is None or self.app_name == '__main__':
            return os.getcwd()
        if hasattr(loader, 'get_filename'):
            filepath = loader.get_filename(self.app_name)
        else:
            # Fall back to imports.
            __import__(self.app_name)
            mod = sys.modules[self.app_name]
            filepath = getattr(mod, '__file__', None)
            if filepath is None:
                raise RuntimeError('No root path can be found for the provided '
                                   'module "%s".  This can happen because the '
                                   'module came from an import hook that does '
                                   'not provide file name information or because '
                                   'it\'s a namespace package.  In this case '
                                   'the root path needs to be explicitly '
                                   'provided.' % self.app_name)
        return os.path.dirname(os.path.abspath(filepath))

    def _get_debug(self):
        return self.config['DEBUG']

    def _set_debug(self, value):
        self.config['DEBUG'] = value

    debug = property(_get_debug, _set_debug)
    del _get_debug, _set_debug

    def get_env(self):
        return os.environ.get('FLASK_ENV') or 'production'

    def get_debug_flag(self):
        val = os.environ.get('FLASK_DEBUG')
        if not val:
            return self.get_env() == 'development'
        return val.lower() not in ('0', 'false', 'no')

    def make_config(self):
        defaults = dict(self.default_config)
        defaults['ENV'] = self.get_env()
        defaults['DEBUG'] = self.get_debug_flag()
        return self.config_class(self.root_path, defaults)

    def config_from_object(self, obj):
        self._config_source = obj
        self.config.from_object(obj)

    @property
    def lambda_environment(self):
        return {}

    def get_function_name(self, stage="dev"):
        return "%s-%s-%s" % (self.app_name, stage, self.index_lambda_function.name)

    def register_lambda_function(self, func, name=None):
        if not name:
            name = func.__name__
        lambda_func = LambdaFunction(func, name)
        self.register_pure_lambda_function(lambda_func)

    def register_pure_lambda_function(self, lambda_func):
        assert isinstance(lambda_func, LambdaFunction)
        for decorator in self.decorators:
            lambda_func = decorator(lambda_func)
        if lambda_func.name in self._pure_lambda_functions:
            raise ValueError("Can not register repeated function!")
        self._pure_lambda_functions[lambda_func.name] = lambda_func

    def lambda_function(self, name=None):
        def _register_lambda_function(lambda_func):
            return self.register_lambda_function(lambda_func, name)
        return _register_lambda_function

    def run(self, name=None):
        def index(event, context):
            function_name = event.pop("function_name", None)
            if not function_name:
                raise LambdaHandleError("function name not provide!")
            if function_name not in self._pure_lambda_functions:
                raise LambdaHandleError("function not defined!")
            return self._pure_lambda_functions[function_name](event, context)

        self.index_lambda_function = LambdaFunction(index, name or "index")
        try:
            sys.modules["app"].index = self.index_lambda_function
        except KeyError:
            sys.modules["__main__"].index = self.index_lambda_function
        self.init_routes()

    def init_routes(self):
        path = "/2015-03-31/functions/%s/invocations" % self.get_function_name()
        self._add_route(path, self.index_lambda_function, methods=["POST"])

    def route(self, path, **kwargs):
        def _register_view(view_func):
            self._add_route(path, view_func, **kwargs)
            return view_func
        return _register_view

    def _add_route(self, path, view_func, **kwargs):
        assert isinstance(view_func, LambdaFunction)
        name = kwargs.pop('name', view_func.name)
        methods = kwargs.pop('methods', ['GET'])
        api_key_required = kwargs.pop('api_key_required', None)
        content_types = kwargs.pop('content_types', ['application/json'])
        if not isinstance(content_types, list):
            raise ValueError('In view function "%s", the content_types '
                             'value must be a list, not %s: %s'
                             % (name, type(content_types), content_types))
        if kwargs:
            raise TypeError('TypeError: route() got unexpected keyword '
                            'arguments: %s' % ', '.join(list(kwargs)))
        if path in self.routes:
            raise ValueError(
                "Duplicate path: '%s' detected for route: '%s'\n" % (path, name)
            )
        self.routes.setdefault(path, dict())
        for method in methods:
            if method in self.routes[path]:
                raise ValueError(
                    "Duplicate method: '%s' detected for route: '%s'\n"
                    "between view functions: \"%s\" and \"%s\". A specific "
                    "method may only be specified once for "
                    "a particular path." % (
                        method, path, self.routes[path][method].view_name, name)
                )
            self.routes[path][method] = RouteEntry(view_func, name, path, method,
                                                   api_key_required, content_types)

    def __call__(self, event, context):
        try:
            response = self.index_lambda_function(event, context)
            if not isinstance(response, Response):
                response = Response(body=response)
        except LambdaHandleError as ex:
            response = Response(body={'Code': ex.__class__.__name__,
                                      'Message': str(ex)},
                                status_code=ex.STATUS_CODE)
            self.logger.error(traceback.format_exc())
        except Exception as ex:
            self.logger.error(str(ex))
            self.logger.error(traceback.format_exc())
            headers = {}
            if self.debug:
                self.logger.debug("Caught exception for %s", event["function_name"], exc_info=True)
                stack_trace = ''.join(traceback.format_exc())
                body = stack_trace
                headers['Content-Type'] = 'text/plain'
            else:
                body = {'Code': 'InternalServerError',
                        'Message': 'An internal server error occurred.'}
            response = Response(body=body, headers=headers, status_code=500)
            signals.lambda_invoke_exception.send(self, exc_info=sys.exc_info(),
                                                 event=event, context=context)
        return response.to_dict()

    def include(self, modules):
        if not isinstance(modules, (tuple, list)):
            raise ValueError("modules must be list values!")
        for import_path in modules:
            __import__(import_path)


def register_function(*sub, **opts):

    def inner_task_cls(**kwargs):
        def entangle(func):
            function_name = func.__name__
            if function_name in LambdaSls.__pre_lambda_functions__:
                raise ValueError("Can not register repeated function!")
            LambdaSls.__pre_lambda_functions__[function_name] = LambdaFunction(
                func, function_name, config=kwargs)
            return func
        return entangle

    if len(sub) == 1:
        if callable(sub[0]):
            return inner_task_cls(**opts)(*sub)
        raise TypeError("argument 1 to @task() must be a callable")
    if sub:
        raise TypeError(
            "@task() takes exactly 1 argument ({0} given)".format(
                sum([len(sub), len(opts)])))
    return inner_task_cls(**opts)
