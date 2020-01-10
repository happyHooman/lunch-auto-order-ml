import math
import numpy as np


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.layers = []
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(NeuronLayer(self.layer_sizes[i + 1], self.layer_sizes[i]))
        self.cost = 0

    def predict(self, input_array):
        if len(input_array) != self.layer_sizes[0]:
            err = f'Your input {input_array} does not match defined input layer size: {self.layer_sizes[0]}'
            raise ValueError(err)
        tmp = input_array
        for k in range(len(self.layers)):
            print('layer', k)
            tmp = self.layers[k].forward(tmp)
        return self.layers[-1].out

    def train(self, inputs, expected_output):
        self.predict(inputs)
        self.cost = 0

        for i in range(self.layer_sizes[-1]):
            self.layers[-1].err[i] = self.layers[-1].out[i] - expected_output[i]
            self.cost += (self.layers[-1].err[i] ** 2) / 2

        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i - 1].err = self.layers[i].train(self.layers[i - 1].out)

    def inspect(self):
        layer_number = 0
        for layer in self.layers:
            layer_number += 1
            print('\n\nLayer', layer_number)
            print('=' * 142)
            print(" ".ljust(8), end='')
            for k in range(len(layer.b)):
                print(str(k).rjust(8), end='')

            print('\nbiases:'.ljust(9), end='')
            for b in np.around(layer.b, decimals=2):
                print(str(b).rjust(8), end='')

            print('\n\nneurons:', end='')
            k = 0
            for n in np.transpose(layer.w):
                k += 1
                for p in np.around(n, decimals=2):
                    print(str(p).rjust(8), end='')
                print(f'\n{k}'.ljust(9), end='')
            print(' ', end='\r')
            print(' ')
            print('output:'.ljust(8), end='')
            for o in np.around(layer.out, decimals=2):
                print(str(o).rjust(8), end='')
            print('\n\nerror:'.ljust(10), end='')
            for e in np.around(layer.err, decimals=2):
                print(str(e).rjust(8), end='')
            print(' ')


class NeuronLayer:
    def __init__(self, size, previous_layer_size):
        self.size = size
        self.pls = previous_layer_size

        # self.w = np.random.random((self.size, self.pls))
        # self.b = np.random.random(self.size)
        # todo remove below lines and uncomment above lines
        self.w = np.array([[.5, .5, .5]])
        self.b = np.array([.5])

        self.out = [0] * self.size
        self.err = [0] * self.size
        self.learning_rate = .5
        self.activation = 'softplus'

    def forward(self, inputs):
        for i in range(self.size):
            total = self.b[i]
            for j in range(self.pls):
                total += inputs[j] * self.w[i][j]
            self.out[i] = self.squash(total)
        return self.out

    def squash(self, z):
        if self.activation == 'sigmoid':
            return 1 / (1 + math.exp(-z))
        elif self.activation == 'relu':
            return max([0, z])
        elif self.activation == 'softsign':
            return z / (1 + abs(z))
        elif self.activation == 'softplus':
            return math.log(1 + math.exp(z))

    def get_derivative(self, i):
        if self.activation == 'sigmoid':
            return self.out[i] * (1 - self.out[i])
        elif self.activation == 'relu':
            # todo de terminat aici
            return 0 if self.out[i] < 0 else self.out[i]
        elif self.activation == 'softsign':
            # todo de terminat aici
            return 1
        elif self.activation == 'softplus':
            # todo de terminat aici
            return 1

    def train(self, inputs):
        return_error = [0] * self.pls
        for i in range(self.size):
            # the derivative of the activation function of the current layer
            # derivative = self.out[i] * (1 - self.out[i])
            derivative = self.get_derivative(i)
            delta = self.err[i] * derivative

            for j in range(self.pls):
                return_error[j] += delta * self.w[i][j]
                self.w[i][j] -= delta * inputs[j] * self.learning_rate

            self.b[i] -= delta * self.learning_rate
        return return_error
