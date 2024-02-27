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

    @staticmethod
    def sigmoid_derivative(x):
        s = NeuralNetwork.sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def cost(x, target):
        return np.square(x - target).sum()

    @staticmethod
    def cost_derivative(x, target):
        return 2 * (x - target)

    def eval(self, v):
        for layer in self.layers:
            v = NeuralNetwork.sigmoid(np.dot(v, layer.weights) + layer.biases)
        return v

    def backpropagation(self, x, target):
        gradient_w = []
        gradient_b = []

        # обход вперёд с сохранением промежуточных значений
        activation = x
        activations = [x]
        zs = []
        for layer in self.layers:
            z = np.dot(activation, layer.weights) + layer.biases
            zs.append(z)
            activation = NeuralNetwork.sigmoid(activation)
            activations.append(activation)

        # вычисление градиента
        delta = NeuralNetwork.cost_derivative(activations[-1], target) * NeuralNetwork.sigmoid_derivative(zs[-1])
        gradient_b.append(delta)
        gradient_w.append(np.dot(delta, activations[-2].transpose()))
        for i in range(len(self.layers) - 2, -1, -1):
            z = zs[i]
            delta = np.dot(self.layers[i + 1].weights.transpose(), delta) * NeuralNetwork.sigmoid_derivative(z)
            gradient_b[i] = delta
            gradient_w[i] = np.dot(delta, activations[i - 1].transpose())

        # т.к. дельты слоёв добавлялись в противоположном порядке, нужно перевернуть
        gradient_b.reverse()
        gradient_w.reverse()
        return gradient_b, gradient_w

    def train(self, training_data, iterations=1000, learning_rate=0.1, batch_size=10):
        pass
