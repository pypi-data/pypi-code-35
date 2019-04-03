from importlib.abc import FileLoader
from types import ModuleType
import weakref as weak
import logging
import sys
from functools import wraps
from contextvars import copy_context, ContextVar
from importlib import import_module
import devconfig

_log = logging.getLogger(__name__)

def strip_spec(spec, fields=()):
    return dict(((k,(v if not hasattr(v, '__dict__') else weak.ref(v)))
                                            for (k,v) in vars(spec).items()
                                            if not k in fields
                                            and not isinstance(v, (bool, type(None)))))

class YAMLFileLoader(FileLoader):
    def create_module(self, spec):
        return  ModuleType(spec.name)

    def exec_module(self, module):
        try:
            devconfig.context.push()
            with open(module.__spec__.origin, 'r') as stream:
                for document in devconfig.documents(stream):
                    _log.debug(f'{module.__spec__.name}', extra=strip_spec(module.__spec__, fields=('name', )))
                    document.loader.module = {
                        'package': module.__package__,
                        'spec': strip_spec(module.__spec__)
                    }
                    module.__dict__.update(document.loader.construct_document(document))
        finally:
            devconfig.context.pop()

    def get_filename(self, fullname):
        return os.path.basename(fullname)

    def get_source(fullname):
        return 'notimplemented'


_sys_modules = ContextVar('devconfig_sys_modules_context')
def contextual(*names):
    def sys_modules_context(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def _ctx(names):
                sys.modules = dict(((k,v) for (k,v) in sys.modules.items() if not k in names))
                for name in names:
                    sys.modules[name] = import_module(name)
                return func(*args, **kwargs)
            ctx = copy_context()
            _sys_modules.set(sys.modules)
            imported_names = [name for name in names if name in sys.modules]
            _log.debug('push', extra={'modules': imported_names})
            try:
                return ctx.run(_ctx, imported_names)
            finally:
                _log.debug('pop', extra={'modules': imported_names})
                sys.modules = _sys_modules.get()
        return wrapper
    return sys_modules_context
