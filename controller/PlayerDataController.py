from .DataController import DataController, CONTROLLERS
from model import PlayerData

import pandas as pd

class PlayerDataController(DataController):
    def __init__(self):
        self.records = []
        self.data_frame = None

    def _setup_dataframe(self):
        self.data_frame = pd.DataFrame([r.to_dict() for r in self.records])
        self.sensitivity_frame = pd.DataFrame([r.sensitivity for r in self.records])

    def load_data(self, data):
        self.clear_records()
        for i in data:
            record = PlayerData(i)
            if record.score == 0:
                continue
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
    
    def get_column_value_count(self, column):
        return self.data_frame[column].value_counts()
    
    def get_column(self, column):
        return self.data_frame[column]
    
    def get_sensitivity(self):
        return self.sensitivity_frame