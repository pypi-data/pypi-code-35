import abc

import numpy as np

__all__ = ['NodeParamView', 'EdgeParamView']

# delegate almost all magic methods to the full array
# (omit in-place ops + a few others like __len__ that we will special
# case)
_delegated_mms = ['abs', 'add', 'and', 'array', 'bool', 'complex',
                  'contains', 'copy', 'deepcopy', 'divmod', 'eq',
                  'float', 'floordiv', 'format', 'ge', 'gt',
                  'index', 'int', 'invert', 'iter', 'le', 'lshift',
                  'lt', 'matmul', 'mod', 'mul', 'ne', 'neg', 'or',
                  'pos', 'pow', 'radd', 'rand', 'rdivmod', 'reduce',
                  'reduce_ex', 'repr', 'rfloordiv', 'rlshift', 'rmatmul',
                  'rmod', 'rmul', 'ror', 'rpow', 'rrshift', 'rsub',
                  'rtruediv', 'rxor', 'sizeof', 'str', 'sub', 'truediv',
                  'xor']


def delegated_to_numpy(method_name):
    def wrapped(self, *args, **kwargs):
        arr = self.array
        return getattr(arr, method_name)(*args, **kwargs)

    return wrapped


class ParamViewMeta(abc.ABCMeta):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        for mm in _delegated_mms:
            mm = f"__{mm}__"
            setattr(cls, mm, delegated_to_numpy(mm))


class ParamView(object, metaclass=ParamViewMeta):

    def __init__(self, net, param, default=None):
        self._net = net
        self._param = param
        self._default = default

    def __len__(self):
        return len(self._net)

    def __getattr__(self, attr):
        return getattr(self.array, attr)

    @abc.abstractmethod
    def __getitem__(self, key):
        pass

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass

    @property
    @abc.abstractmethod
    def shape(self):
        pass

    @property
    @abc.abstractmethod
    def array(self):
        pass


class NodeParamView(ParamView):

    def __getitem__(self, node):
        return self._net.nodes[node].get(self._param, self._default)

    def __setitem__(self, node, value):
        self._net.nodes[node][self._param] = value

    @property
    def shape(self):
        n = len(self)
        return (n,)

    @property
    def array(self):
        return np.array([self[node] for node in self._net])


class EdgeParamView(ParamView):

    def __getitem__(self, edge):
        return self._net.edges[edge].get(self._param, self._default)

    def __setitem__(self, edge, value):
        self._net.edges[edge][self._param] = value

    @property
    def shape(self):
        n = len(self)
        return (n, n)

    @property
    def array(self):
        # map node to idx
        idx = dict((node, i) for i, node in enumerate(self._net))
        arr = np.zeros(self.shape)
        for u in self._net:
            for v in self._net.neighbors(u):
                arr[idx[u], idx[v]] = self[u, v]
        return arr
