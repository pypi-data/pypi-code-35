from collections import MutableMapping

from paramnet.exceptions import ParametrizedNetworkError, NodeParameterError, \
    EdgeParameterError

__all__ = []
__all__.extend([
    'Dict',
    'OuterDict',
    'AttrDict',
    'NodeDict',
    'NodeAttrDict',
    'AdjlistOuterDict',
    'AdjlistInnerDict',
    'EdgeAttrDict',
])


class Dict(MutableMapping):
    """ base nested dictionary class for paramnet """
    _child_cls = None

    def __init__(self, data=None, instance=None):
        self._data = data
        self._instance = instance

    def __setitem__(self, key, value):
        if isinstance(value, MutableMapping) and self._child_cls is not None:
            value = self._child_cls(data=value, instance=self._instance)
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getattr__(self, attr):
        return getattr(self._data, attr)


class AttrDict(Dict):
    """ dict that prevents specified keys from being removed
        once added """

    _exception = ParametrizedNetworkError
    _node_edge = ""

    @property
    def required_attrs(self):
        return getattr(self._instance, f"_{self._node_edge}_params")

    def __delitem__(self, k):
        if k in self._equired_attrs:
            raise self._exception(
                f"Can't delete required {self._node_edge} attribute '{k}'.")
        super().__delitem__(k)

    def clear(self):
        if self.required_attrs:
            raise self._exception(
                f"Can't clear the following required {self._node_edge} "
                f"attributes: {self.required_attrs}")
        super().clear()

    def pop(self, k, default=None):
        if k in self.required_attrs:
            if default is None:
                raise self._exception(
                    f"Can't pop required {self._node_edge} attribute "
                    f"'{k}'.")
            return default
        return super().pop(k, default)

    def popitem(self):
        k, v = super().popitem()
        if k in self.required_attrs:
            self[k] = v
            raise self._exception(
                f"Cannot pop required {self._node_edge} attribute '{k}' "
                f"for {self._el}")

    def has_all_attrs(self):
        return set(self.required_attrs) <= set(self)


class OuterDict(Dict):

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self._name]

    def __set__(self, instance, value):
        instance.__dict__[self._name] = self.__class__(data=value,
                                                       instance=instance)


class NodeAttrDict(AttrDict):
    _exception = NodeParameterError
    _node_edge = "node"


class EdgeAttrDict(AttrDict):
    _exception = EdgeParameterError
    _node_edge = "edge"


class AdjlistInnerDict(Dict):
    _child_cls = EdgeAttrDict


class NodeDict(OuterDict):
    _child_cls = NodeAttrDict


class AdjlistOuterDict(OuterDict):
    _child_cls = AdjlistInnerDict
