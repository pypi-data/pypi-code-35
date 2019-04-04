from neup.layers.graph import LayerGraph, join
from neupy.layers.base import BaseLayer


__all__ = ('copy', 'repeat')


def _copy_layer(layer, keep_variables=False):
    parameters = layer.get_params()
    return layer.__class__(**parameters)


def copy(network, keep_variables=False):
    if isinstance(network, BaseLayer):
        return _copy_layer(network, keep_variables)
    raise NotImplementedError("")


def repeat(network, n, keep_variables=False):
    networks = [copy(network, keep_variables) for _ in range(n)]
    return join(*networks)


def update(network, rules):
    pass
