from dataclasses import dataclass
from .AbstractData import AbstractData

@dataclass
class PlayerData(AbstractData):
    def __init__(self, data):
        self.shots_fired = data.get("shotsFired",0)
        self.shots_hit = data.get("shotsHit",0)
        self.accuracy = self.shots_hit / self.shots_fired if self.shots_fired > 0 else 0
        self.score = data.get("score",0)
        self.device = data.get("device","")
        self.device_make = data.get("deviceMake","")
        self.crosshair_index = data.get("crossHairIndex")
        self._id = data["_id"]["$oid"]
        self.modifiers_collected = data.get("modifiersCollected", {})
        self.sensitivity = data.get("sensitivity", {})
        self.mapping = {
            "Player Records":1,
            "Combined Score":self.score, 
            "Total Shots Fired":self.shots_fired, 
            "Total Shots Hit":self.shots_hit
        }
    
    def aggregate_labels():
        return  ("Player Records", "Combined Score", "Total Shots Fired", "Total Shots Hit")

    def get_aggregate_data(self, label):
        return self.mapping[label]
    
    def to_dict(self):
        return {
            "_id":self._id,
            "shots_fired":self.shots_fired,
            "shots_hit":self.shots_hit,
            "accuracy":self.accuracy,
            "score":self.score,
            "device":self.device,
            "device_make":self.device_make,
            "crosshair_index":self.crosshair_index,
        }