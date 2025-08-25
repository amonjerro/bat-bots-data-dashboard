from abc import ABC, abstractmethod

class AbstractData:
    @staticmethod
    def aggregate_labels(self):
        pass

    @abstractmethod
    def get_aggregate_data(self, label):
        pass