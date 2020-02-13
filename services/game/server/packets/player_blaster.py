from typing import Dict
from server.packets.packet import Packet


class PlayerBlasterPacket(Packet):

    def __init__(self, player_id: str):
        self.player_id = player_id

    def encode(self) -> Dict:
        packet = super().encode()
        packet["player_id"] = self.player_id
        return packet

    @staticmethod
    def decode(data: Dict) -> Packet:
        return PlayerBlasterPacket(
            player_id=data["player_id"],
        )

    @staticmethod
    def get_type() -> str:
        return "player_blast"
