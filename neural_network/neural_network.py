import json
import numpy as np
from dataclasses import dataclass


class NeuralNetwork:
    @dataclass
    class __Layer:
        weights: any
        biases: any

    def __init__(self, input_size: int, output_size: int, hidden_size: int, hidden_count: int, random_seed: int = None):
        if random_seed is not None:
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
    def from_file(filepath: str):
        layers = json.load(open(filepath, "r"))
        network = NeuralNetwork.__new__(NeuralNetwork)
        network.layers = [NeuralNetwork.__Layer(
            weights=np.array(layer["weights"]),
            biases=np.array(layer["biases"])
        ) for layer in layers]
        return network

    def save_to_file(self, filepath: str):
        json.dump(
            [{
                "weights": layer.weights.tolist(),
                "biases": layer.biases.tolist()
            } for layer in self.layers],
            open(filepath, "w")
        )

    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def __sigmoid_derivative(x):
        s = NeuralNetwork.__sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def __cost(x, target):
        return np.square(x - target).sum()

    @staticmethod
    def __cost_derivative(x, target):
        return 2 * (x - target)

    def eval(self, v):
        for layer in self.layers:
            v = self.__sigmoid(np.dot(v, layer.weights) + layer.biases)
        return v

    def __backpropagation(self, x, target):
        gradient_w = []
        gradient_b = []

        # обход вперёд с сохранением промежуточных значений
        activation = x
        activations = [x]
        zs = []
        for layer in self.layers:
            z = np.dot(activation, layer.weights) + layer.biases
            zs.append(z)
            activation = self.__sigmoid(z)
            activations.append(activation)
        cost = self.__cost(activation, target)

        # вычисление градиента
        # TODO: правильно сделать перемножение матриц и векторов
        delta = self.__cost_derivative(activations[-1], target) * self.__sigmoid_derivative(zs[-1])
        gradient_b.append(delta)
        gradient_w.append(np.dot(delta, activations[-2].transpose()))
        for i in range(len(self.layers) - 2, -1, -1):
            z = zs[i]
            delta = np.dot(self.layers[i + 1].weights.transpose(), delta) * self.__sigmoid_derivative(z)
            gradient_b.append(delta)
            gradient_w.append(np.dot(delta, activations[i - 1].transpose()))

        # Т.к. градиенты слоёв добавлялись в противоположном порядке, нужно перевернуть
        gradient_b.reverse()
        gradient_w.reverse()
        return gradient_b, gradient_w, cost

    def train(self, training_data, iterations=1000, learning_rate=0.1, batch_size=10, seed=None, testing_data=None, logger=None):
        for iteration in range(iterations):
            if seed is not None:
                np.random.seed(seed)
            training_data = training_data.to_numpy()
            np.random.shuffle(training_data)
            # разбиваем данные на части
            mean_cost = 0
            for j in range(0, len(training_data), batch_size):
                batch = training_data[j:j+batch_size]
                # вычисляем средний градиент для каждой части
                gradient_b_sum = [np.zeros(layer.biases.shape) for layer in self.layers]
                gradient_w_sum = [np.zeros(layer.weights.shape) for layer in self.layers]
                for row in batch:
                    x, target = np.array([row[1:]]), np.array([row[0:1]])
                    gradient_b, gradient_w, cost = self.__backpropagation(x, target)
                    mean_cost += cost
                    for i in range(len(self.layers)):
                        gradient_b_sum[i] += gradient_b[i]
                        gradient_w_sum[i] += gradient_w[i]
                # применяем на веса и смещения
                step_size = learning_rate / len(batch)
                for i in range(len(self.layers)):
                    self.layers[i].biases -= gradient_b_sum[i] * step_size
                    self.layers[i].weights -= gradient_w_sum[i] * step_size
            mean_cost /= len(training_data)
            if testing_data is None:
                if logger is None:
                    print(f"Итерация {iteration} выполнена, средняя ошибка: {mean_cost}")
                else:
                    logger.report_scalar("Loss", "Train", iteration=iteration, value=mean_cost)
            else:
                # тестируем и вычисляем среднюю ошибку
                test_mean_cost = 0
                for x, target in testing_data:
                    test_mean_cost += self.__cost(self.eval(x), target)
                test_mean_cost /= len(testing_data)
                if logger is None:
                    print(f"Итерация {iteration} выполнена, средняя ошибка: {mean_cost}, средняя ошибка тестов: {test_mean_cost}")
                else:
                    logger.report_scalar("Loss", "Train", iteration=iteration, value=mean_cost)
                    logger.report_scalar("Loss", "Test", iteration=iteration, value=test_mean_cost)
