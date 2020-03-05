from typing import Dict
from server.packets.packet import Packet


class GameJoinPacket(Packet):

    def __init__(self, player_id: str, game_id: str, player_name: str, color: str):
        self.player_id = player_id
        self.game_id = game_id
        self.player_name = player_name
        self.color = color

    def encode(self) -> Dict:
        packet = super().encode()
        packet["player_id"] = self.player_id
        packet["game_id"] = self.game_id
        packet["player_name"] = self.player_name
        packet["color"] = self.color
        return packet

    @staticmethod
    def decode(data: Dict) -> Packet:
        return GameJoinPacket(
            player_id=data['player_id'],
            game_id=data['game_id'],
            player_name=data['player_name'],
            color=data['color']
        )

    @staticmethod
    def get_type() -> str:
        return "join_game"
