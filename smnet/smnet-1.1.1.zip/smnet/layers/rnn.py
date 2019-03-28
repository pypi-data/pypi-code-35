# -----------------
# SMNet
# Written by smarsu
# -----------------

"""Reccurent nerual network layer"""

import numpy as np
from ..blob import Tensor, Variable
from .. import layer as nn
from ..ops.param_op import *

class Rnn():
    def __init__(self):
        pass
        self.act_map = {
            'relu': nn.relu,
            'tanh': nn.tanh,
        }

    
    def __call__(self, inputs, state, hidden_size=None, input_size=None, act='tanh'):
        """
        Args:
            inputs: List of Tensor(), e.g. [Tensor(), ..., Tensor()]
                Every times input of RNN.
            state: The initial state of RNN, in default, it should be zeros.
            hidden_size: The hidden units size of RNN.
        Returns:
            outputs:
            states:
        """
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        weight = Variable(data=glorot_uniform((hidden_size + input_size, hidden_size)))
        bias = Variable(data=np.zeros((hidden_size, )))
        outputs = []
        states = []
        for inp in inputs:
            output, state = self._op(inp, state, weight, bias)
            outputs.append(output)
            states.append(state)
        return outputs, states


    def _op(self, inp, state, weight, bias):
        """TODO(smarsu): Add bias to matmul"""
        data_x = nn.concat([inp, state], axis=-1)
        data_y = nn.add(nn.matmul(data_x, weight), bias)
        data_y = nn.tanh(data_y)
        return data_y, data_y  # Note: Did here need duplicate?


rnn = Rnn()


class Lstm():
    def __init__(self):
        pass


    def __call__(self, inputs, state, hidden_size=None, input_size=None, forget_bias=1.):
        assert len(inputs) >= 1, 'you must need inputs, inputs length is {}'.format(len(inputs))
        glorot_data = Variable(glorot_uniform((hidden_size + input_size, hidden_size * 4)))
        bias = Variable(data=np.zeros((hidden_size * 4, )))
        forget_bias = Tensor(data=forget_bias)

        outputs = []
        states = []
        for inp in inputs:
            output, state = self._op(inp, state, glorot_data, bias, forget_bias)
            outputs.append(output)
            states.append(state)
        return outputs, states


    def _op(self, inp, state, glorot_data, bias, forget_bias):
        c, h = state
        data_x = nn.concat([inp, h], -1)

        # i, j, f, o
        i, j, f, o = nn.split(
            nn.add(nn.matmul(data_x, glorot_data), bias), 4, -1)

        i = nn.sigmoid(i)
        j = nn.tanh(j)
        f = nn.sigmoid(nn.add(f, forget_bias))
        o = nn.sigmoid(o)

        new_c = nn.add(
            nn.multiply(c, f),
            nn.multiply(i, j),
        )
        new_h = nn.multiply(o, nn.tanh(new_c))
        return new_h, (new_c, new_h)


lstm = Lstm()
