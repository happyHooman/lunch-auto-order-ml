import math

import numpy as np

from ML.get_user_training_data import get_words

words = ['<PAD>', '<UNK>'] + get_words()


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.layers = []
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(NeuronLayer(self.layer_sizes[i + 1], self.layer_sizes[i]))
        self.word_embeddings = {key: np.random.random(4) for key in words}
        self.cost = 0

    def predict(self, input_array):
        if type(input_array[0]) == str:
            input_array = np.hstack((self.name_to_embedding(input_array[0]), input_array[1:]))
        for k in range(len(self.layers)):
            tmp = self.layers[k].forward(input_array if k == 0 else tmp)
        return self.layers[-1].out

    def name_to_embedding(self, name):
        return np.hstack([self.word_embeddings[x] for x in name.split()])

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

        print('\nWord embeddings:')
        for key, value in self.word_embeddings.items():
            val = ''
            for x in np.around(value, decimals=2):
                val += str(x).rjust(7)
            print(key.rjust(12), val)

    def train(self, inputs, expected_output):
        name = inputs[0]
        inputs = np.hstack((self.name_to_embedding(inputs[0]), inputs[1:]))
        self.predict(inputs)
        self.cost = 0

        for i in range(self.layer_sizes[-1]):
            self.layers[-1].err[i] = self.layers[-1].out[i] - expected_output[i]
            self.cost += (self.layers[-1].err[i] ** 2) / 2

        for i in range(len(self.layers) - 1, 0, -1):
            self.layers[i - 1].err = self.layers[i].train(self.layers[i - 1].out)
        embedding_err = self.layers[0].train(inputs)
        self.update_word_embeddings(embedding_err, name)

    def update_word_embeddings(self, err, dishname):
        vector_size = 4
        index = 0
        for word in dishname.split():
            for i in range(vector_size):
                delta = err[index * vector_size + i]
                self.word_embeddings[word][i] -= delta
            index += 1


class NeuronLayer:
    def __init__(self, size, previous_layer_size):
        self.size = size
        self.pls = previous_layer_size
        self.w = np.random.random((self.size, self.pls)) * .01
        self.b = np.random.random(self.size) * .01
        self.out = [0] * self.size
        self.err = [0] * self.size
        self.learning_rate = .5

    def forward(self, inputs):
        for i in range(self.size):
            total = self.b[i]
            for j in range(self.pls):
                total += inputs[j] * self.w[i][j]
            self.out[i] = self.squash(total)
        return self.out

    @staticmethod
    def squash(z, activation='sigmoid'):
        if activation == 'sigmoid':
            return 1 / (1 + math.exp(-z))
        elif activation == 'relu':
            return max([0, z])

    def train(self, inputs):
        return_error = [0] * self.pls
        for i in range(self.size):
            delta = self.err[i] * self.out[i] * (1 - self.out[i])

            for j in range(self.pls):
                return_error[j] += delta * self.w[i][j]
                self.w[i][j] -= delta * inputs[j] * self.learning_rate

            self.b[i] -= delta * self.learning_rate
        return return_error
