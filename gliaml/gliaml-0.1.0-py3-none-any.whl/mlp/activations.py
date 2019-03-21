"""
Copyright 2019 Archie Shahidullah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    """
    Actual derivative: S'(x) = S(x)(1-S(x)) but the inputs have already gone
    through the sigmoid function.
    """
    return x * (1 - x)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    """
    Actual derivative: tanh'(x) = 1 - (tanh(x))^2 but logic same as sigmoid
    derivative
    """
    return 1 - x ** 2


def relu(x):
    return x * (x > 0)


def relu_derivative(x):
    return 1 * (x > 0)


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def softmax_derivative(x):
    return x * (1 - x)


functions = {
    1: sigmoid,
    2: tanh,
    3: relu,
    4: softmax
}

derivatives = {
    1: sigmoid_derivative,
    2: tanh_derivative,
    3: relu_derivative,
    4: softmax_derivative
}
