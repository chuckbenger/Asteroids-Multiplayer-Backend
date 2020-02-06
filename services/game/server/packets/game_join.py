from typing import Dict
from server.packets.packet import Packet


class GameJoinPacket(Packet):

    def __init__(self, player_id: str, game_id: str):
        self.player_id = player_id
        self.game_id = game_id

    def encode(self) -> Dict:
        packet = super().encode()
        packet["player_id"] = self.player_id
        packet["game_id"] = self.game_id
        return packet

    @staticmethod
    def get_type() -> str:
        return "join_game"
