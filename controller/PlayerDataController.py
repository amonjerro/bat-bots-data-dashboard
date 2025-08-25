from .DataController import DataController, CONTROLLERS
from model import PlayerData

import pandas as pd

class PlayerDataController(DataController):
    def __init__(self):
        self.records = []
        self.data_frame = None

    def _setup_dataframe(self):
        self.data_frame = pd.DataFrame([r.to_dict() for r in self.records])

    def load_data(self, data):
        self.clear_records()
        for i in data:
            self.records.append(PlayerData(i))
        self._setup_dataframe()

    def clear_records(self):
        del self.records[:]
        self.data_frame = None

    def get_model_aggregate_labels(self):
        return PlayerData.aggregate_labels()
    
    def get_aggregate_data(self, label):
        return sum([r.get_aggregate_data(label) for r in self.records])
    
    def get_controller_identifier(self):
        return CONTROLLERS.PLAYER