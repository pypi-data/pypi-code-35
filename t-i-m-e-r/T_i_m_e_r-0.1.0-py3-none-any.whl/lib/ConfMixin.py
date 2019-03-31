class ConfMixin:
    def __init__(self):
        self._confs = {}

    def _register_conf(self, *, name, func_get=None, func_set=None, override=False):
        if func_get is None and func_set is None:
            return

        if (name in self._confs) and (not override):
            raise ValueError('Configuration name %s already existed' % name)

        self._confs[name] = (func_get, func_set)

    def _unregister_conf(self, name):
        if name in self._confs:
            del self._confs[name]

    def configure(self, **kwargs):
        if len(kwargs) == 0:
            return {name: func_get() for name, (func_get, _) in self._confs.items() if func_get is not None}

        for name, value in kwargs.items():
            if name not in self._confs:
                raise AttributeError('Unknown configuration name %s' % name)

            _, func_set = self._confs[name]
            if func_set is not None:
                func_set(value)

    def configuration_names(self):
        return list(self._confs.keys())
