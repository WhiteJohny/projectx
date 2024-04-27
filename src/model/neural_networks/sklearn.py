import clearml
import pandas as pd
import numpy as np
import joblib
from sklearn.neural_network import MLPRegressor
from .base import BaseNetwork


class SKLearn(BaseNetwork):
    def __init__(self, input_size: int, output_size: int, hidden_size: int, hidden_count: int, random_seed: int = None):
        self.network = MLPRegressor(
            hidden_layer_sizes=np.full((hidden_count,), hidden_size),
            activation="logistic",
            solver="sgd",
            random_state=random_seed,
            verbose=True
        )

    FILE_EXTENSION = ".joblib"

    @staticmethod
    def from_file(filepath: str):
        net = MLPRegressor.__new__(MLPRegressor)
        net.network = joblib.load(filepath)
        return net

    def save_to_file(self, filepath: str):
        joblib.dump(self.network, filepath)

    def train(self,
              training_data: pd.DataFrame,
              iterations: int = 500,
              learning_rate: float = 0.001,
              batch_size: int = 10,
              seed: int = None,
              testing_data: pd.DataFrame = None,
              logger: clearml.Logger = None
              ):
        training_data = training_data.to_numpy()
        x, y = training_data[:, 1:], training_data[:, 0].reshape(-1, 1)
        self.network.max_iter = iterations
        self.network.learning_rate_init = learning_rate
        self.network.batch_size = batch_size
        self.network.random_state = seed
        self.network = self.network.fit(x, y)

    def eval(self, v):
        return self.network.predict(v)
