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
import sys
from gliaml.activations import functions, derivatives


class NetworkLayer:

    def __init__(self, num_inputs, num_neurons, activations, bias=False):
        # weights from [-1, 1) by shifting continuous uniform distribution
        self.weights = 2 * np.random.random((num_inputs, num_neurons)) - 1
        # activations is a list corresponding to the dictionary above for nodes
        self.activations = activations
        self.bias = bias
        # bias weights initialise as an array of zeros
        self.b = np.zeros((num_neurons,))


class NeuralNetwork:

    def __init__(self, *layers):
        # variable number of layers stored as a tuple
        self.layers = layers

    @staticmethod
    def mean_squared_error(actual, target):
        """
        This function implements the half-mean-squared error cost function.

        :param actual: NumPy array of the network's actual outputs
        :param target: NumPy array of the network's target outputs

        :return: the derivative of the half-mean squared error function
                 with respect to the actual outputs
        """
        return actual - target

    @staticmethod
    def cross_entropy(actual, target):
        """
        This function implements the cross-entropy cost function.

        :param actual: NumPy array of the network's actual outputs
        :param target: NumPy array of the network's target outputs

        :return: the derivative of the cross-entropy cost function
                 with respect to the actual outputs
        """
        if actual.ndim == 1:
            error = np.zeros(len(actual))

            for i in range(0, len(actual)):
                if actual[i] == 1:
                    error[i] = 0
                    continue

                elif actual[i] == 0:
                    error[i] = sys.maxsize
                    continue

                error[i] = -1 * ((target[i] * (1 / actual[i]) +
                                  (1 - target[i]) * (1 / (1 - actual[i]))))

        else:
            error = np.zeros(actual.shape)

            for i in range(0, len(actual)):
                for j in range(0, len(actual[0])):
                    if actual[i][j] == 1:
                        error[i][j] = 0
                        continue

                    elif actual[i][j] == 0:
                        error[i][j] = sys.maxsize
                        continue

                    error[i][j] = -1 * ((target[i][j] * (1 / actual[i][j]) +
                                         (1 - target[i][j]) * (1 / (1 - actual[i][j]))))

        return error

    def think(self, inputs):
        """
        This method implements forward propagation for either one, or an arbitrary amount
        of training samples.

        :param inputs: NumPy array containing the inputs to the network

        :return: outputs: an array containing the outputs of each layer
        """
        outputs = []
        n = 1

        if inputs.ndim == 1:  # if there is only one input sample

            for layer in self.layers:

                if n == 1:  # if it is the first layer
                    temp = np.dot(inputs, layer.weights)

                    # for loop applies respective activation to each output
                    # each value in the temp array is the weighted sum of a node
                    for i, activation in enumerate(layer.activations):
                        b = layer.b[i]
                        temp[i] = functions[activation](temp[i] + b)

                    outputs.append(temp)
                    n += 1

                else:  # for any layer after the first
                    temp = np.dot(outputs[n-2], layer.weights)

                    for i, activation in enumerate(layer.activations):
                        b = layer.b[i]
                        temp[i] = functions[activation](temp[i] + b)

                    outputs.append(temp)
                    n += 1

        else:  # for an arbitrary amount of input samples

            for layer in self.layers:

                if n == 1:  # first layer
                    temp = np.dot(inputs, layer.weights)

                    # columns are a node's weighted sums for input samples
                    for i, activation in enumerate(layer.activations):
                        b = np.repeat(layer.b[i], np.size(temp, 0))
                        temp[:, i] = functions[activation](temp[:, i] + b)

                    outputs.append(temp)
                    n += 1

                else:  # any layer but first
                    temp = np.dot(outputs[n-2], layer.weights)

                    for i, activation in enumerate(layer.activations):
                        b = np.repeat(layer.b[i], np.size(temp, 0))
                        temp[:, i] = functions[activation](temp[:, i] + b)

                    outputs.append(temp)
                    n += 1
                    # outputs is an NumPy array of the outputs of each layer

        # e.g. [output1, output2] where output1 = [o1, o2, ...] for each node
        return outputs

    def train(self, train_inputs, train_outputs, num_iterations, cost_function,
              learning_rate=1, bias_learning_rate=1):
        """
        This function implements the generic backpropagation algorithm with the
        specified cost function for one, or an arbitrary amount of training samples.

        :param train_inputs: NumPy array containing training inputs
        :param train_outputs: NumPy array containing target outputs
        :param num_iterations: Number of iterations to perform backpropagation
        :param cost_function: The specified cost function
        :param learning_rate: Learning rate hyperparameter
        :param bias_learning_rate: Bias learning rate hyperparameter

        :return: none
        """
        lr = learning_rate
        blr = bias_learning_rate

        for iteration in range(num_iterations):
            outputs = self.think(train_inputs)
            deltas = []
            num_layers = len(outputs)

            for i in range(num_layers - 1, -1, -1):
                temp = outputs[i].copy()
                layer = self.layers[i]

                if i == num_layers - 1:  # if final layer
                    # calculates the error with the specified cost function
                    error = cost_function(temp, train_outputs)

                    if temp.ndim == 1:  # if only one training sample

                        # applies respective derivatives to node output
                        for j, activation in enumerate(layer.activations):
                            temp[j] = derivatives[activation](temp[j])

                    else:
                        # respective derivatives but for multiple samples
                        for j, activation in enumerate(layer.activations):
                            temp[:, j] = derivatives[activation](temp[:, j])

                    deltas.append(error * temp)

                else:  # if not final layer
                    next_layer = self.layers[i+1]
                    error = deltas[num_layers-i-2].dot(next_layer.weights.T)

                    if temp.ndim == 1:
                        for j, activation in enumerate(layer.activations):
                            temp[j] = derivatives[activation](temp[j])

                    else:
                        for j, activation in enumerate(layer.activations):
                            temp[:, j] = derivatives[activation](temp[:, j])

                    # deltas is a NumPy array of the deltas for each layer
                    # Note: is in reverse order to outputs array
                    deltas.append(error * temp)

            for k in range(num_layers - 1, -1, -1):
                layer = self.layers[k]

                if k == 0:  # if first layer
                    adjustment = lr * train_inputs.T.dot(deltas[num_layers-k-1])
                    layer.weights -= adjustment

                    if layer.bias:  # only updates if bias is enabled
                        layer.b -= blr * np.ones((1, np.size(deltas[num_layers-k-1],
                                                             0))).dot(deltas[num_layers-k-1])[0]

                else:  # if not first layer
                    adjustment = lr * outputs[k-1].T.dot(deltas[num_layers-k-1])
                    layer.weights -= adjustment

                    if layer.bias:
                        layer.b -= blr * np.ones((1, np.size(deltas[num_layers-k-1],
                                                             0))).dot(deltas[num_layers-k-1])[0]

    def train_mean_squared_error(self, train_inputs, train_outputs, num_iterations,
                                 learning_rate=1, bias_learning_rate=1):
        """
        This function implements backpropagation with the half-mean-squared cost function for
        one, or an arbitrary amount of training samples.

        :param train_inputs: NumPy array containing training inputs
        :param train_outputs: NumPy array containing target outputs
        :param num_iterations: Number of iterations to perform backpropagation
        :param learning_rate: Learning rate hyperparameter
        :param bias_learning_rate: Bias learning rate hyperparameter

        :return: none
        """
        self.train(train_inputs, train_outputs, num_iterations,
                   self.mean_squared_error, learning_rate, bias_learning_rate)

    def train_cross_entropy(self, train_inputs, train_outputs, num_iterations,
                            learning_rate=1, bias_learning_rate=1):
        """
        This function implements backpropagation with the cross-entropy loss cost function (also
        known as negative log-likelihood) for one, or an arbitrary amount of training samples.

        :param train_inputs: NumPy array containing training inputs
        :param train_outputs: NumPy array containing target outputs
        :param num_iterations: Number of iterations to perform backpropagation
        :param learning_rate: Learning rate hyperparameter
        :param bias_learning_rate: Bias learning rate hyperparameter

        :return: none
        """
        self.train(train_inputs, train_outputs, num_iterations,
                   self.cross_entropy, learning_rate, bias_learning_rate)
