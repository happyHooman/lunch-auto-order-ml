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
            raise ValueError('Your input does not match defined input layer size.')
        tmp = input_array
        for k in range(len(self.layers)):
            tmp = self.layers[k].forward(tmp)
        return self.layers[-1].output

    def calculate_cost(self, expected_output):
        self.cost = 0
        for i in range(self.layer_sizes[-1]):
            self.layers[-1].err[i] = self.layers[-1].output[i] - expected_output[i]
            self.cost += (self.layers[-1].err[i] ** 2) / 2

    def train(self, inputs, expected_output):
        self.predict(inputs)
        self.calculate_cost(expected_output)

        # from the last to the second layer update weights and biases
        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i - 1].err = self.layers[i].train(self.layers[i - 1].output)
        # update weights and biases in the first layer
        feedback_err = self.layers[0].train(inputs)
        return feedback_err

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
            for b in np.around(layer.b, decimals=4):
                print(str(b).rjust(8), end='')

            print('\n\nneurons:', end='')
            k = 0
            for n in np.transpose(layer.w):
                k += 1
                for p in np.around(n, decimals=4):
                    print(str(p).rjust(8), end='')
                print(f'\n{k}'.ljust(9), end='')
            print(' ', end='\r')
            print(' ')
            print('output:'.ljust(8), end='')
            for o in np.around(layer.output, decimals=4):
                print(str(o).rjust(8), end='')
            print('\n\nerror:'.ljust(10), end='')
            for e in np.around(layer.err, decimals=4):
                print(str(e).rjust(8), end='')
            print(' ')


class NeuronLayer:
    def __init__(self, size, previous_layer_size, activation='softplus'):
        self.size = size
        self.pls = previous_layer_size
        self.w = np.random.random((self.size, self.pls))
        self.b = np.random.random(self.size)
        self.total_net_input = [0] * self.size
        self.output = [0] * self.size
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
        self.output = [self.squash(o) for o in self.total_net_input]
        return self.output

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
        """Returns the derivative of the squash function"""
        tni = self.total_net_input
        if self.activation == 'sigmoid':
            out = self.output
            return out[i] * (1 - out[i])
        elif self.activation == 'relu':
            return 0 if tni[i] <= 0 else tni[i]
        elif self.activation == 'softsign':
            return 1 / (1 + abs(tni[i])) ** 2
        elif self.activation == 'softplus':
            return 1 / (1 + math.exp(-tni[i]))

    def train(self, inputs):
        """Back propagation"""
        previous_layer_error = [0] * self.pls
        for i in range(self.size):
            delta = self.err[i] * self.get_derivative(i)

            for j in range(self.pls):
                previous_layer_error[j] += delta * self.w[i][j]
                self.w[i][j] -= delta * inputs[j] * self.learning_rate
            self.b[i] -= delta * self.learning_rate
        return previous_layer_error
