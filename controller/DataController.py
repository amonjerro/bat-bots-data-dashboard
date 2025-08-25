from abc import ABC, abstractmethod
from enum import Enum

CONTROLLERS = Enum("Controllers", [("GAME", 1), ("PLAYER", 2)])

class DataController(ABC):
    @abstractmethod
    def load_data(self, data):
        pass

    @abstractmethod
    def clear_records(self):
        pass

    @abstractmethod
    def get_model_aggregate_labels(self):
        pass

    @abstractmethod
    def get_aggregate_data(self, label):
        pass

    @abstractmethod
    def get_controller_identifier(self):
        pass