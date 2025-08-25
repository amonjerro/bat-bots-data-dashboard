from dataclasses import dataclass
from .AbstractData import AbstractData

@dataclass
class GameData(AbstractData):
    def __init__(self, data):
        self.game_mode = data["gameMode"]
        self.duration = data["duration"]
        self.player_count = data["playerCount"]
        self.bats_shot = data["batsShot"]
        self.total_bats_shot = sum(self.bats_shot.values())
        self.bats_spawned = data["batsSpawned"]
        self.total_bats_spawned = sum(self.bats_spawned.values())
        self.players = []
        for i in data["playerData"]["insertedIds"].values():
            self.players.append(i["$oid"])

        self.mapping = {
            "Total Games Played":1,
            "Total Duration":self.duration,
            "Total Bats Spawned":self.total_bats_spawned,
            "Total Bats Shot": self.total_bats_shot
        }

    def aggregate_labels():
        return ("Total Games Played", "Total Duration", "Total Bats Spawned","Total Bats Shot")
    
    def get_aggregate_data(self, label):
        return self.mapping[label]

    def to_dict(self):
        return {
            "game_mode":self.game_mode,
            "duration":self.duration,
            "player_count":self.player_count,
            "total_bats_shot":self.total_bats_shot,
            "total_bats_spawned":self.total_bats_spawned
        }
