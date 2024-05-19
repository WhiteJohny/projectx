import clearml
import pandas as pd
import numpy as np
import joblib
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
from .base import BaseNetwork


class SKLearn(BaseNetwork):
    def __init__(self, input_size: int, output_size: int, hidden_size: int, hidden_count: int, random_seed: int = None):
        self.net = MLPRegressor(
            hidden_layer_sizes=np.full((hidden_count,), hidden_size),
            activation="logistic",
            solver="sgd",
            random_state=random_seed,
            verbose=True
        )

    FILE_EXTENSION = ".joblib"

    @staticmethod
    def from_file(filepath: str):
        skl = MLPRegressor.__new__(MLPRegressor)
        skl.net = joblib.load(filepath)
        return skl

    def save_to_file(self, filepath: str):
        joblib.dump(self.net, filepath)

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
        self.net.max_iter = iterations
        self.net.learning_rate_init = learning_rate
        self.net.batch_size = batch_size
        self.net.random_state = seed
        self.net = self.net.fit(x, y)
        if testing_data is not None:
            testing_data = testing_data.to_numpy()
            x, y_true = testing_data[:, 1:], testing_data[:, 0]
            y_pred = np.array([self.net.predict(np.array([i])) for i in x])
            errors = y_pred - y_pred
            scatter_data = np.hstack(
                (np.atleast_2d(np.arange(0, len(y_pred))).T, errors.reshape(len(y_pred), 1))
            )
            logger.report_scatter2d("Error", "series", scatter_data, 0)
            logger.report_single_value("Mean Absolute Error", metrics.mean_absolute_error(y_true, y_pred))
            logger.report_single_value("Max Error", metrics.max_error(y_true, y_pred))

    def eval(self, v):
        return self.net.predict(v)
