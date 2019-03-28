# -----------------
# SMNet Layer
# Written by smarsu
# -----------------

"""
Some useful neural network layers.
"""

import logging
import numpy as np
from numba import jit

from .blob import Tensor, Variable
from .ops import array_op
from .net import sm


class Layer(object):
    """Network is stacked by layers.
    
    If we want to customize layers, we need to implement the following three functions:

    _prebuilt(self, a, b, ...):
        Prepare for the computation of this layer.

    forward(self):
        Layer operate, compute output by input.

    backward(self):
        Optimizer operate, compute the gradient of the current layer by the gradient of the top layer.
    """

    _name_id = 0

    def __init__(self, stop_grad=False, name='Layer'):
        sm.add_layer(self)
        
        self.stop_grad = stop_grad
        self._name = self._get_name(name)


    def _get_name(self, name):
        Layer._name_id += 1
        return '_'.join([name, str(Layer._name_id)])

    
    def _tensor(self, v):
        if isinstance(v, Tensor) or isinstance(v, Variable):
            return v
        else:
            return Tensor(v)


class Matmul(Layer):
    """TODO(samrsu): Merge bias to FullConnect"""

    def __init__(self, a, b):
        super(Matmul, self).__init__()
        self._prebuilt(a, b)


    def _prebuilt(self, a, b):
        self.a = self._tensor(a)
        self.b = self._tensor(b)
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(np.matmul(a, b))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """
        a_grad = res_grad * b.T
        """
        # 1. Prepare data
        b = self.b.data

        # 2. Compute and add grad
        self.a.add_grad(np.matmul(grad, b.T))


    def _compute_grad_b(self, grad):
        """
        b_grad = a.T * grad
        TODO(smarsu): Understand it.
        """
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and add grad
        self.b.add_grad(np.matmul(a.T, grad))


def matmul(a, b):
    return Matmul(a, b).res


class Add(Layer):
    def __init__(self, a, b):
        super(Add, self).__init__()
        self._prebuilt(a, b)
    

    def _prebuilt(self, a, b):
        self.a = self._tensor(a)
        self.b = self._tensor(b)
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a + b)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """For the NHWC data format, bias should collect gradients in the same way."""
        # 1. Prepare grad
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)
        else:
            grad = grad.copy()

        # 2. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare grad
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)
        else:
            grad = grad.copy()

        # 2. Add grad
        self.b.add_grad(grad)


def add(a, b):
    return Add(a, b).res


class Subtract(Layer):
    def __init__(self, a, b):
        super(Subtract, self).__init__()
        self._prebuilt(a, b)
    

    def _prebuilt(self, a, b):
        self.a = self._tensor(a)
        self.b = self._tensor(b)
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare input data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a - b)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        """For the NHWC data format, bias should collect gradients in the same way."""
        # 1. Prepare grad
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)
        else:
            grad = grad.copy()

        # 2. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare grad
        grad = -grad
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 2. Add grad
        self.b.add_grad(grad)

    
def subtract(a, b):
    return Subtract(a, b).res


class Multiply(Layer):
    def __init__(self, a, b):
        super(Multiply, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        self.a = self._tensor(a)
        self.b = self._tensor(b)
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a * b)
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        b = self.b.data

        # 2. Compute grad
        grad = grad * b
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.a.add_grad(grad)
    

    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute grad
        grad = grad * a
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.b.add_grad(grad)


def multiply(a, b):
    return Multiply(a, b).res


class Divide(Layer):
    def __init__(self, a, b):
        super(Divide, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        self.a = self._tensor(a)
        self.b = self._tensor(b)
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(a / b)
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        b = self.b.data

        # 2. Compute grad
        grad = grad / b
        if grad.shape != self.a.shape:
            grad = np.reshape(grad, [-1] + list(self.a.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.a.add_grad(grad)
    

    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = grad * a / (-b * b)
        if grad.shape != self.b.shape:
            grad = np.reshape(grad, [-1] + list(self.b.shape))
            grad = np.sum(grad, axis=0)

        # 3. Add grad
        self.b.add_grad(grad)


def divide(a, b):
    return Divide(a, b).res


class Sigmoid(Layer):
    def __init__(self, a):
        super(Sigmoid, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()

    
    def forward(self):
        """Shall we add limit here to avoid overflow?"""
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.sigmoid(a))
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        res = self.res.data

        # 2. Compute grad
        grad = grad * res * (1 - res)

        # 3. Add grad
        self.a.add_grad(grad)


def sigmoid(a):
    return Sigmoid(a).res


class Relu(Layer):
    def __init__(self, a):
        super(Relu, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(np.maximum(0, a))

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute grad
        grad = np.where(a > 0, grad, 0)
        
        # 3. Add grad
        self.a.add_grad(grad)


def relu(a):
    return Relu(a).res


class Tanh(Layer):
    def __init__(self, a):
        super(Tanh, self).__init__()
        self._prebuilt(a)

    
    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.tanh(a))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        # 1. Prepare data
        res = self.res.data

        # 2. Compute grad
        grad = (1 - np.square(res)) * grad

        # 3. Add grad
        self.a.add_grad(grad)


def tanh(a):
    return Tanh(a).res


class Mse(Layer):
    def __init__(self, a, b):
        super(Mse, self).__init__()
        self._prebuilt(a, b)

    
    def _prebuilt(self, a, b):
        logging.warning('sm.nn.mse actually calculates L2_loss instead of MSE.')

        self.a = a
        self.b = b
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute and feed result
        self.res.feed(0.5 * np.square(a - b))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)
        self._compute_grad_b(grad)

    
    def _compute_grad_a(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = (a - b) * grad

        # 3. Add grad
        self.a.add_grad(grad)

    
    def _compute_grad_b(self, grad):
        # 1. Prepare data
        a = self.a.data
        b = self.b.data

        # 2. Compute grad
        grad = (b - a) * grad

        # 3. Add grad
        self.b.add_grad(grad)


def mse(a, b):
    return Mse(a, b).res


class Concat(Layer):
    def __init__(self, values, axis):
        super(Concat, self).__init__()
        self._prebuilt(values, axis)

    
    def _prebuilt(self, values, axis):
        self.values = values
        self.axis = axis
        self.res = Tensor()
    

    def forward(self):
        # 1. Prepare data
        values = [v.data for v in self.values]
        axis = self.axis

        # 2. Compute and feed result
        self.res.feed(np.concatenate(values, axis))


    def backward(self):
        grad = self.res.grad
        self._compute_grad_values(grad)
        

    def _compute_grad_values(self, grad):
        # 1. Prepare data
        axis = self.axis

        # 2. Compute grad
        split_idx = []
        cur_idx = 0
        for blob in self.values:
            cur_idx += blob.shape[axis]
            split_idx.append(cur_idx)
        grads = np.split(grad, split_idx, axis)
        grads.pop()

        # 3. Add grad
        for value, grad in zip(self.values, grads):
            value.add_grad(grad)


def concat(values, axis):
    return Concat(values, axis).res


class Stack(Layer):
    def __init__(self, values, axis, stop_grad, name):
        super(Stack, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(values, axis)

    
    def _prebuilt(self, values, axis):
        self.values = values
        self.axis = axis
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        values = [blob.data for blob in self.values]
        axis = self.axis

        # 2. Compute and feed result
        self.res.feed(np.stack(values, axis))

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_values(grad)


    def _compute_grad_values(self, grad):
        # 1. Prepare data
        axis = self.axis

        # 2. Compute grad
        grads = np.split(grad, list(range(1, grad.shape[axis] + 1)), axis)
        grads.pop()
        grads = [np.squeeze(grad, axis=axis) for grad in grads]

        # 3. Add grad
        for blob, grad in zip(self.values, grads):
            blob.add_grad(grad)


def stack(values, axis, stop_grad=False, name='Stack'):
    return Stack(values, axis, stop_grad, name).res


class Split(Layer):
    def __init__(self, value, num_or_size_splits, axis):
        super(Split, self).__init__()
        self._prebuilt(value, num_or_size_splits, axis)

    
    def _prebuilt(self, value, num_or_size_splits, axis):
        self.value = value
        self.num_or_size_splits = num_or_size_splits
        self.axis = axis

        num = num_or_size_splits if isinstance(num_or_size_splits, int) else len(num_or_size_splits)
        self.res = [Tensor() for _ in range(num)]

    
    def forward(self):
        """Splits a tensor into sub tensors.

        ```py
        >>> x = sm.Tensor(range(9))
        >>> sm.nn.split(x, 3)
        [Tensor([ 0.,  1.,  2.]), Tensor([ 3.,  4.,  5.]), Tensor([ 6.,  7.,  8.])]

        >>> x = sm.Tensor(range(8))
        >>> sm.nn.split(x, [3, 5, 6, 10])
        [Tensor([ 0.,  1.,  2.]),
        Tensor([ 3.,  4.]),
        Tensor([ 5.]),
        Tensor([ 6.,  7.]),
        Tensor([], dtype=float64)]
        ```
        
        """
        # 1. Prepare data
        value = self.value.data
        num_or_size_splits = self.num_or_size_splits
        axis = self.axis

        # 2. Compute result
        if isinstance(num_or_size_splits, list):
            sub_values = np.split(value, num_or_size_splits, axis)
            sub_values.pop()
        else:
            sub_values = np.split(value, num_or_size_splits, axis)

        # 3. Feed result
        for res, sub_value in zip(self.res, sub_values):
            res.feed(sub_value)

    
    def backward(self):
        grads = [blob.grad for blob in self.res]
        self._compute_grad_value(grads)


    def _compute_grad_value(self, grads):
        # 1. Prepare data
        axis = self.axis

        # 2. Compute and add grad
        self.value.add_grad(np.concatenate(grads, axis))


def split(value, num_or_size_splits, axis):
    return Split(value, num_or_size_splits, axis).res


class Pad(Layer):
    def __init__(self, tensor, paddings, constant_values=0, stop_grad=False, name='Pad'):
        super(Pad, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(tensor, paddings, constant_values)

    
    def _prebuilt(self, tensor, paddings, constant_values):
        """
        TODO(smarsu): Multi type of paddings
        """
        self.tensor = tensor
        self.paddings = paddings
        self.constant_values = constant_values
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        tensor = self.tensor.data
        paddings = self.paddings
        constant_values = self.constant_values

        # 2. Compute and feed result
        self.res.feed(np.pad(tensor, paddings, 'constant', constant_values=constant_values))

    
    def backward(self):
        """
        We will not compute the grad of `paddings`
        """
        grad = self.res.grad
        self._compute_grad_tensor(grad)


    def _compute_grad_tensor(slef, grad):
        # 1. Prepare data
        paddings = self.paddings

        # 2. Compute grad
        grad_shape = grad.shape
        grad = eval(
            'grad[{}]'.format(
                ','.join(['{}:{}'.format(l, grad_shape[idx]-r) for idx, (l, r) in enumerate(paddings)])
            )
        )

        # 3. Add grad
        self.tensor.add_grad(grad)


def pad(tensor, paddings, constant_values=0, stop_grad=False, name='Pad'):
    return Pad(tensor, paddings, constant_values, stop_grad, name).res


class Reshape(Layer):
    def __init__(self, tensor, shape, stop_grad=False, name='Reshape'):
        super(Reshape, self).__init__(stop_grad=stop_grad, name=name)
        self._prebuilt(tensor, shape)

    
    def _prebuilt(self, tensor, shape):
        self.tensor = tensor
        self.shape = shape
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        tensor = self.tensor.data
        shape = self.shape

        # 2. Compute and feed result
        self.res.feed(np.reshape(tensor, shape))

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_tensor(grad)


    def _compute_grad_tensor(self, grad):
        # 1. Prepare data
        tensor_shape = self.tensor.shape

        # 2. Compute and add grad
        self.tensor.add_grad(np.reshape(grad, tensor_shape))


def reshape(tensor, shape, stop_grad=False, name='Reshape'):
    return Reshape(tensor, shape, stop_grad, name).res


class Embedding_lookup(Layer):
    def __init__(self, params, ids, stop_grad):
        super(Embedding_lookup, self).__init__(stop_grad=stop_grad)
        self._prebuilt(params, ids)

    
    def _prebuilt(self, params, ids):
        """
        sm.nn.embedding_lookup will automatically add a row(all zeros) at the end of params, it represents the pad character.

        Args:
            params: Tensor(), shape like [num_voca, num_feature]
            ids: Tensor(), shape like [batch, time_step] or [batch]
        Returns:
            res: Tensor(), shape like [batch(, time_step), num_feature]
        """
        self.params = params
        self.ids = ids
        self.res = Tensor()

        # Prepare pad data
        """params = params.data
        num_voca, num_feature = params.shape
        self.params.init_feed(np.concatenate([params, np.zeros((1, num_feature))], 0))"""

    
    def forward(self):
        """Looks up `ids` in a list of embedding tensors.

        The params had been padded
        """
        # 1. Prepare data
        params = self.params.data
        ids = self.ids.data

        # 2. Compute and feed result
        self.res.feed(params[ids])

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_params(grad)


    def _compute_grad_params(self, grad):
        """TODO(smarsu): Remove loop
        
        grad have shape [batch(, time_step), num_feature]
        ids have shape [batch(, time_step)]
        """
        # 1. Prepare data
        ids = self.ids.data

        # 2. Compute and add grad
        if self.params._grad is 0:
            self.params._grad = np.zeros(self.params.shape, dtype=self.params.dtype)

        num_voca, num_feature = self.params.shape
        grad = np.reshape(grad, [-1, num_feature])
        ids = ids.flatten()

        _embedding_lookup_backpropagation(ids, grad, self.params._grad, num_voca)

        #for id, part_grad in zip(ids.flatten(), grad):
        #    if id >= num_voca: continue  # The weight of the pad will not be updated
        #    self.params._grad[id] += part_grad


@jit(nopython=True, parallel=True, fastmath=True)
def _embedding_lookup_backpropagation(ids, grad, params_grad, num_voca):
    for i in range(len(ids)):
        if ids[i] >= num_voca: continue  # The weight of the pad will not be updated
        params_grad[ids[i]] += grad[i]  # [id] is quicker than [id, :]


def embedding_lookup(params, ids, stop_grad=False):
    return Embedding_lookup(params, ids, stop_grad=stop_grad).res


class Softmax(Layer):
    def __init__(self, a):
        super(Softmax, self).__init__()
        self._prebuilt(a)
    

    def _prebuilt(self, a):
        self.a = a
        self.res = Tensor()


    def forward(self):
        # 1. Prepare data
        a = self.a.data

        # 2. Compute and feed result
        self.res.feed(array_op.softmax(a))
    

    def backward(self):
        grad = self.res.grad
        self._compute_grad_a(grad)


    def _compute_grad_a(self, grad):
        raise NotImplementedError


def softmax(a):
    return Softmax(a).res


class Softmax_log_cross_entropy(Layer):
    def __init__(self, labels, logits):
        super(Softmax_log_cross_entropy, self).__init__()
        self._prebuilt(labels, logits)
    

    def _prebuilt(self, labels, logits):
        """
        The dim always be -1
        """

        logging.warning('sm.nn.softmax_log_cross_entropy always calculates the value of the -1 dimension')

        self.labels = labels
        self.logits = logits
        self.res = Tensor()

    
    def forward(self):
        # 1. Prepare data
        labels = self.labels.data
        logits = self.logits.data

        # 2. Compute result
        softmax_logits = array_op.softmax(logits)
        neg_log_logits = -np.log(softmax_logits)
        #cross_entropy = np.sum(labels * neg_log_logits, -1, keepdims=True)
        cross_entropy = labels * neg_log_logits

        self.softmax_logits = softmax_logits
        self.neg_log_logits = neg_log_logits

        # 3. Feed result
        self.res.feed(cross_entropy)

    
    def backward(self):
        grad = self.res.grad
        self._compute_grad_lables(grad)
        self._compute_grad_logits(grad)

    
    def _compute_grad_lables(self, grad):
        """Actually, we need not compute lables grad."""
        # 1. Prepare data
        neg_log_logits = self.neg_log_logits

        # 2. Compute and add grad
        self.labels.add_grad(neg_log_logits * grad)

    
    def _compute_grad_logits(self, grad):
        """
        For grad[..., i], it affect grad[..., :] by the way [a, ..., k - 1, ..., n]
        """
        # 1. Prepare data
        labels = self.labels.data
        softmax_logits = self.softmax_logits

        # 2. Compute and add grad
        for i in range(labels.shape[-1]):
            softmax_logits_i = np.copy(softmax_logits)
            softmax_logits_i[..., i] -= 1
            self.logits._grad += grad[..., i:i+1] * labels[..., i:i+1] * softmax_logits_i


    def _compute_grad_logits_v2(self, a, b, grad):
        """THIS FUNCTION IS DEPRECATED, use _compute_grad_logits instead"""
        b = b.data

        softmax_a = array_op.softmax(a.data)

        diff = np.zeros(a.shape)

        for i in range(a.shape[-1]):
            _softmax_a = np.copy(softmax_a)
            _softmax_a[..., i:i+1] = _softmax_a[..., i:i+1] - 1
            diff += b[..., i:i+1] * _softmax_a

        # Here grad maybe 1
        diff = diff * grad

        diff = np.where(softmax_a > 1e-10, diff, 0)

        self._add_diff(a, diff)
        return diff


def softmax_log_cross_entropy(labels, logits):
    return Softmax_log_cross_entropy(labels, logits).res
