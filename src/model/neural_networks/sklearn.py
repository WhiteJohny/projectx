import clearml
import pickle
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from .base import BaseNetwork


class SKLearn(BaseNetwork):
    def __init__(self, input_size: int, output_size: int, hidden_size: int, hidden_count: int, random_seed: int = None):
        self.network = MLPRegressor(
            hidden_layer_sizes=np.full((hidden_count,), hidden_size),
            activation="sigmoid",
            solver="sgd",
            random_state=random_seed,
            verbose=True
        )

    @staticmethod
    def from_file(filepath: str):
        net = MLPRegressor.__new__(MLPRegressor)
        with open(filepath, "w") as f:
            net.network = pickle.load(f)
        return net

    def save_to_file(self, filepath: str):
        with open(filepath, "w") as f:
            pickle.dump(self.network, f)

    def train(self,
              training_data: pd.DataFrame,
              iterations: int = 1000,
              learning_rate: float = 0.1,
              batch_size: int = 10,
              seed: int = None,
              testing_data: pd.DataFrame = None,
              logger: clearml.Logger = None
              ):
        training_data = training_data.to_numpy()
        y, x = np.hsplit(training_data, 1)
        self.network.max_iter = iterations
        self.network.learning_rate_init = learning_rate
        self.network.batch_size = batch_size
        self.network.random_state = seed
        self.network = self.network.fit(x, y)

    def eval(self, v):
        return self.network.predict(v)
