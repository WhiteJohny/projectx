import json
import time
import clearml
import pandas as pd
import numpy as np
from dataclasses import dataclass
from .base import BaseNetwork


class CustomNN(BaseNetwork):
    @dataclass
    class __Layer:
        weights: any
        biases: any

    def __init__(self, input_size: int, output_size: int, hidden_size: int, hidden_count: int, random_seed: int = None):
        if random_seed is not None:
            np.random.seed(random_seed)
        self.layers = []
        if hidden_count > 0:
            self.layers.append(self.__Layer(
                weights=np.random.randn(hidden_size, input_size),
                biases=np.zeros(hidden_size)
            ))
            for i in range(hidden_count - 1):
                self.layers.append(self.__Layer(
                    weights=np.random.randn(hidden_size, hidden_size),
                    biases=np.zeros(hidden_size)
                ))
            self.layers.append(self.__Layer(
                weights=np.random.randn(output_size, hidden_size),
                biases=np.zeros(output_size)
            ))
        else:
            self.layers.append(self.__Layer(
                weights=np.random.randn(output_size, input_size),
                biases=np.zeros(output_size)
            ))

    FILE_EXTENSION = ".json"

    @staticmethod
    def from_file(filepath: str):
        with open(filepath, "r") as f:
            layers = json.load(f)
        network = CustomNN.__new__(CustomNN)
        network.layers = [CustomNN.__Layer(
            weights=np.array(layer["weights"]),
            biases=np.array(layer["biases"])
        ) for layer in layers]
        return network

    def save_to_file(self, filepath: str):
        with open(filepath, "w") as f:
            json.dump([{
                "weights": layer.weights.tolist(),
                "biases": layer.biases.tolist()
            } for layer in self.layers], f)

    @staticmethod
    def __sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def __sigmoid_derivative(x):
        s = CustomNN.__sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def __cost(x, target):
        return np.square(x - target).sum()

    @staticmethod
    def __cost_derivative(x, target):
        return 2 * (x - target)

    def eval(self, v):
        for layer in self.layers:
            v = self.__sigmoid(np.dot(layer.weights, v) + layer.biases)
        return v

    def __backpropagation(self, x, target):
        gradient_w = []
        gradient_b = []

        # обход вперёд с сохранением промежуточных значений
        activation = x
        activations = [x]
        zs = []
        for layer in self.layers:
            z = np.dot(layer.weights, activation) + layer.biases
            zs.append(z)
            activation = self.__sigmoid(z)
            activations.append(activation)
        cost = self.__cost(activation, target)

        # вычисление градиента
        delta = self.__cost_derivative(activations[-1], target) * self.__sigmoid_derivative(zs[-1])
        gradient_b.append(delta)
        gradient_w.append(np.dot(delta[:, np.newaxis], activations[-2][np.newaxis, :]))
        for i in range(2, len(self.layers) + 1):
            delta = np.dot(self.layers[-i + 1].weights.transpose(), delta) * self.__sigmoid_derivative(zs[-i])
            gradient_b.append(delta)
            gradient_w.append(np.dot(delta[:, np.newaxis], activations[-i - 1][np.newaxis, :]))

        # Т.к. градиенты слоёв добавлялись в противоположном порядке, нужно перевернуть
        gradient_b.reverse()
        gradient_w.reverse()
        return gradient_b, gradient_w, cost

    def train(self,
              training_data: pd.DataFrame,
              iterations: int = 100,
              learning_rate: float = 0.1,
              batch_size: int = 10,
              seed: int = None,
              testing_data: pd.DataFrame = None,
              logger: clearml.Logger = None
              ):
        training_data = training_data.to_numpy()
        if testing_data is not None:
            testing_data = testing_data.to_numpy()
        if seed is not None:
            np.random.seed(seed)
        for iteration in range(1, iterations + 1):
            mean_cost = 0
            # разбиваем данные на части
            np.random.shuffle(training_data)
            for j in range(0, len(training_data), batch_size):
                batch = training_data[j:j + batch_size]
                # вычисляем средний градиент для каждой части
                gradient_b_sum = [np.zeros(layer.biases.shape) for layer in self.layers]
                gradient_w_sum = [np.zeros(layer.weights.shape) for layer in self.layers]
                for row in batch:
                    x, target = row[1:], row[0:1]
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
                print(f"[{time.strftime('%H:%M:%S')}] Итерация {iteration} выполнена, средняя ошибка: {mean_cost})")
                if logger is not None:
                    logger.report_scalar("Loss", "Train", iteration=iteration, value=mean_cost)
            else:
                # тестируем и вычисляем среднюю ошибку
                test_mean_cost = 0
                for row in testing_data:
                    x, target = row[1:], row[0:1]
                    test_mean_cost += self.__cost(self.eval(x), target)
                test_mean_cost /= len(testing_data)
                print(f"[{time.strftime('%H:%M:%S')}] Итерация {iteration} выполнена, средняя ошибка: {mean_cost}, средняя ошибка тестов: {test_mean_cost}")
                if logger is not None:
                    logger.report_scalar("Loss", "Train", iteration=iteration, value=mean_cost)
                    logger.report_scalar("Loss", "Test", iteration=iteration, value=test_mean_cost)
