from typing import Dict
from server.packets.packet import Packet


class PlayerStatsUpdatePacket(Packet):

    def __init__(self, player_id: str, lives: int, score: int):
        self.player_id = player_id
        self.lives = lives
        self.score = score

    def encode(self) -> Dict:
        packet = super().encode()
        packet['player_id'] = self.player_id
        packet['lives'] = self.lives
        packet['score'] = self.score
        return packet

    @staticmethod
    def decode(data: Dict):
        return PlayerRespawnPacket(
          player_id=data["player_id"],
          lives=data['lives'],
          score=data['score']
        )

    @staticmethod
    def get_type() -> str:
        return "player_stats"

