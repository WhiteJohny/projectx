import numpy as np
from dataclasses import dataclass


class NeuralNetwork:
    @dataclass
    class __Layer:
        weights: any
        biases: any

    def __init__(self, input_size, output_size, hidden_size, hidden_count, random_seed):
        np.random.seed(random_seed)
        self.layers = []
        self.layers.append(self.__Layer(
            weights=np.random.randn(input_size, hidden_size),
            biases=np.zeros((1, hidden_size))
        ))
        for i in range(hidden_count - 1):
            self.layers.append(self.__Layer(
                weights=np.random.randn(hidden_size, hidden_size),
                biases=np.zeros((1, hidden_size))
            ))
        self.layers.append(self.__Layer(
            weights=np.random.randn(hidden_size, output_size),
            biases=np.zeros((1, output_size))
        ))

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def eval(self, inputs):
        v = inputs
        for layer in self.layers:
            v = NeuralNetwork.sigmoid(np.dot(v, layer.weights) + layer.biases)
        return v
