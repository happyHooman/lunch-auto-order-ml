import math
import numpy as np


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.layers = []
        # todo remove predefined weights and bias
        www = [[[.15, .2], [.25, .3]],
               [[.4, .45], [.5, .55]]]
        bbb = [[.35, .35],
               [.6, .6]]
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(NeuronLayer(self.layer_sizes[i + 1], self.layer_sizes[i], www[i], bbb[i]))
        self.cost = 0

    def predict(self, input_array):
        if len(input_array) != self.layer_sizes[0]:
            raise ValueError('Your input does not match defined input layer size.')
        tmp = input_array
        for k in range(len(self.layers)):
            tmp = self.layers[k].forward(tmp)
        return self.layers[-1].get_output()

    def train(self, inputs, expected_output):
        self.predict(inputs)
        # todo make sure cost is calculated properly
        # https://stats.stackexchange.com/questions/154879/a-list-of-cost-functions-used-in-neural-networks-alongside-applications
        self.cost = 0

        # todo: save separately the output and total net input
        for i in range(self.layer_sizes[-1]):
            self.layers[-1].err[i] = self.layers[-1].total_net_input[i] - expected_output[i]
            # todo cost is calculated here
            self.cost += (self.layers[-1].err[i] ** 2) / 2

        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i - 1].err = self.layers[i].train(self.layers[i - 1].total_net_input)

    def inspect(self):
        layer_number = 0

        print('\n\nCost:', self.cost)
        for layer in self.layers:
            layer_number += 1
            print('\nLayer', layer_number)
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
            for o in np.around(layer.total_net_input, decimals=2):
                print(str(o).rjust(8), end='')
            print('\n\nerror:'.ljust(10), end='')
            for e in np.around(layer.err, decimals=2):
                print(str(e).rjust(8), end='')
            print(' ')


class NeuronLayer:
    def __init__(self, size, previous_layer_size, weights, bias, activation='sigmoid'):
        self.size = size
        self.pls = previous_layer_size

        # todo remove predifined wigths and bias
        self.w = weights or np.random.random((self.size, self.pls))
        self.b = bias or np.random.random(self.size)

        self.total_net_input = [0] * self.size
        self.err = [0] * self.size
        self.learning_rate = .5
        self.activation = activation

    def forward(self, inputs):
        for i in range(self.size):
            total = self.b[i]
            for j in range(self.pls):
                total += inputs[j] * self.w[i][j]
            self.total_net_input[i] = total
        return self.get_output()

    def get_output(self):
        return [self.squash(o) for o in self.total_net_input]

    def squash(self, z):
        """Squash the total net input"""
        if self.activation == 'sigmoid':
            return 1 / (1 + math.exp(-z))
        elif self.activation == 'relu':
            return max([0, z])
        elif self.activation == 'softsign':
            return z / (1 + abs(z))
        elif self.activation == 'softplus':
            return math.log(1 + math.exp(z))
        else:
            raise ValueError('Not a valid activation function')

    def get_derivative(self, i):
        """Returns the derivative of the output in respect to total net input"""
        tni = self.total_net_input
        if self.activation == 'sigmoid':
            sig = self.get_output()
            return sig[i] * (1 - sig[i])
        elif self.activation == 'relu':
            return 0 if tni[i] <= 0 else tni[i]
        elif self.activation == 'softsign':
            return 1 / (1 + abs(tni[i])) ** 2
        elif self.activation == 'softplus':
            return 1 / (1 + math.exp(-tni[i]))

    def train(self, inputs):
        """Backpropagation"""
        previous_layer_error = [0] * self.pls
        for i in range(self.size):
            delta = self.err[i] * self.get_derivative(i)

            for j in range(self.pls):
                previous_layer_error[j] += delta * self.w[i][j]
                self.w[i][j] -= delta * inputs[j] * self.learning_rate

            self.b[i] -= delta * self.learning_rate
        return previous_layer_error
