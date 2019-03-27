import abc

import numpy as np

__all__ = ['ParamView', 'NodeParamView', 'EdgeParamView']

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

    def __init__(self, name, net, default=np.nan):
        self._name = name
        self._net = net
        self._default = default

    def __len__(self):
        return len(self._net)

    def __getattr__(self, attr):
        return getattr(self.array, attr)

    @abc.abstractmethod
    def set(self, value):
        pass

    @abc.abstractmethod
    def __getitem__(self, item):
        pass

    @abc.abstractmethod
    def __setitem__(self, item, value):
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

    def __getitem__(self, item):
        def _get(node):
            return self._net.nodes[node].get(self._name, self._default)

        try:
            return _get(item)
        except (KeyError, TypeError):
            nodes = list(item)
            return np.array([_get(node) for node in nodes])

    def __setitem__(self, item, value):
        def _set(node, value):
            self._net.nodes[node][self._name] = value

        if item in self._net.nodes:
            _set(item, value)
        else:
            nodes = list(item)
            if np.isscalar(value):
                for node in nodes:
                    _set(node, value)
            else:
                for node, v in zip(nodes, value):
                    _set(node, v)

    def set(self, value):
        if np.isscalar(value):
            for node in self._net:
                self[node] = value
        else:
            for node, v in zip(self._net.nodes, value):
                self[node] = v

    @property
    def shape(self):
        n = len(self)
        return (n,)

    @property
    def array(self):
        return np.array([self[node] for node in self._net], dtype=np.float64)


class EdgeParamView(ParamView):

    def __getitem__(self, item):
        def _get(edge):
            return self._net.edges[edge].get(self._name, self._default)

        try:
            return _get(item)
        except (KeyError, TypeError):
            edges = list(item)
            return np.array([_get(edge) for edge in edges])

    def __setitem__(self, item, value):
        def _set(edge, value):
            self._net.edges[edge][self._name] = value

        if item in self._net.edges:
            _set(item, value)
        else:
            edges = list(item)
            if np.isscalar(value):
                for edge in edges:
                    _set(edge, value)
            else:
                for edge, v in zip(edges, value):
                    _set(edge, v)

    def set(self, value):
        if np.isscalar(value):
            for edge in self._net.edges():
                self[edge] = value
        else:
            nodes = list(self._net)
            value = np.array(value).reshape(self.shape)
            if not self._net.is_directed() and not np.all(
                    value == value.T):
                raise ValueError(
                    f"Can't set edge param '{self._name}' with a "
                    f"non-symmetric matrix when graph is undirected.")
            for (i, j), v in np.ndenumerate(value):
                node1, node2 = nodes[i], nodes[j]
                if self._net.has_edge(node1, node2):
                    self[node1, node2] = v

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
