from .DataController import DataController, CONTROLLERS
from model import GameData
import pandas as pd

class GameDataController(DataController):
    def __init__(self):
        self.records = []
        self.data_frame = None
        self.bats_shot_frame = None
    
    def _setup_dataframe(self):
        self.data_frame = pd.DataFrame([r.to_dict() for r in self.records])
        self.bats_shot_frame = pd.DataFrame([r.bats_shot for r in self.records])
        self.bats_shot_frame = self.bats_shot_frame.drop("bonus", axis=1)

    def load_data(self, data):
        self.clear_records()
        for i in data:
            self.records.append(GameData(i))
        self._setup_dataframe()
        

    def clear_records(self):
        del self.records[:]
        self.data_frame = None

    def get_model_aggregate_labels(self):
        return GameData.aggregate_labels()

    def get_aggregate_data(self, label):
        return sum([r.get_aggregate_data(label) for r in self.records])

    def get_controller_identifier(self):
        return CONTROLLERS.GAME
    
    def get_column_data(self, column):
        return self.data_frame[column]

    def get_bats_shot(self):
        return self.bats_shot_frame.sum()
    
    def get_value_counts(self, column):
        return self.data_frame[column].value_counts()