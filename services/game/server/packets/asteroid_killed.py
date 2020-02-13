from typing import Dict
from server.packets.packet import Packet


class AsteroidKilledPacket(Packet):

    def __init__(self, asteroid_id: str):
        self.asteroid_id = asteroid_id

    def encode(self) -> Dict:
        packet = super().encode()
        packet["asteroid_id"] = self.asteroid_id
        return packet

    @staticmethod
    def decode(data: Dict) -> Packet:
        return AsteroidKilledPacket(
            asteroid_id=data["asteroid_id"],
        )

    @staticmethod
    def get_type() -> str:
        return "asteroid_killed"
