import pandas as pd
import clearml
from abc import ABC, abstractmethod


class BaseNetwork(ABC):
    @abstractmethod
    def train(self,
              training_data: pd.DataFrame,
              iterations: int = 100,
              learning_rate: float = 0.1,
              batch_size: int = 10,
              seed: int = None,
              testing_data: pd.DataFrame = None,
              logger: clearml.Logger = None
              ):
        pass

    FILE_EXTENSION = ""

    @staticmethod
    @abstractmethod
    def from_file(filepath: str):
        pass

    @abstractmethod
    def save_to_file(self, filepath: str):
        pass

    @abstractmethod
    def eval(self, v):
        pass
