from typing import Dict, List
from server.packets.packet import Packet
from server.asteroid import Asteroid


class GameInitPacket(Packet):

    def __init__(self, asteroids: List[Asteroid]):
        self.asteroids = asteroids

    def encode(self) -> Dict:
        packet = super().encode()
        packet["asteroids"] = [a.to_dict() for a in self.asteroids]
        return packet

    @staticmethod
    def get_type() -> str:
        return "game_init"
