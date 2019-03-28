# -----------------
# SMNet Network
# Written by smarsu
# -----------------

import logging
import numpy as np
from .ops import array_op


def Singleton(cls, _instance={}):
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@Singleton
class Net(object):
    """
    SMNet can only built one graph at a time
    TODO(smarsu): Built multi-graph.
    """

    def __init__(self):
        self._layers = []
        self._backlayers = []

        self._variable = set()
        self._tensor = set()

        self._variable_momentum = {}

        self._check_dtype_time = 0


    def add_layer(self, layer):
        self._layers.append(layer)
        self._backlayers.insert(0, layer)

    
    def add_tensor(self, v):
        self._tensor.add(v)

    
    def add_variable(self, v):
        self._variable.add(v)


    def _check_dtype(self):
        if self._check_dtype_time == 0:
            for v in self._variable.union(self._tensor):
                if v._data.dtype != v.dtype:
                    logging.warning('Data dtype unmatch at layer {}, expect {} but {}'.format(v.name, v.dtype, v._data.dtype))
                if not isinstance(v._grad, int) and v._grad.dtype != v.dtype:
                    logging.warning('Grad dtype unmatch at layer {}, expect {} but {}'.format(v.name, v.dtype, v._grad.dtype))

            self._check_dtype_time += 1


    def _feed_data(self, feed_dict):
        for k, v in feed_dict.items():
            k.init_feed(v)


    def forward(self, feed_dict=None):
        if feed_dict is not None:
            self._feed_data(feed_dict)

        for layer in self._layers:
            layer.forward()


    def backward(self, blobs, lr, momentum, weight_decay):
        """
        TODO(smarsu): Check out why momentum affect the converge. 
        """
        # grad = lr
        for blob in blobs:
            blob.set_grad(np.full(blob.shape, lr, dtype=blob.dtype))

        for layer in self._backlayers:
            if not layer.stop_grad:
                layer.backward()

        if momentum > 0:
            self._momentum_update(momentum)
        if weight_decay > 0:
            self._weight_norm(weight_decay)


    def _momentum_update(self, momentum):
        """Reference: https://arxiv.org/abs/1706.02677v1
        
        Ut+1 = m * Ut + grad
        Wt+1 = Wt - lr * Ut+1
        """
        for v in self._variable:
            self._variable_momentum[v] = v.add_grad(momentum * self._variable_momentum.get(v, 0))
        
    
    def _weight_norm(self, weight_decay):
        for v in self._variable:
            v.add_grad(weight_decay * array_op.l2_loss(v.data))


    def update(self):
        for v in self._variable:
            v.update()
        
        for v in self._variable:
            v.clear_grad()

        for v in self._tensor:
            v.clear_grad()


    def optimize(self, blobs, lr=1., momentum=0., weight_decay=0.):
        self.backward(blobs, lr, momentum, weight_decay)
        self._check_dtype()
        self.update()


sm = Net()
