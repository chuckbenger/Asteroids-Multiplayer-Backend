from typing import Dict
from server.packets.packet import Packet


class GameInitPacket(Packet):

    def __init__(self, asteroids: []):
        self.asteroids = asteroids

    def encode(self) -> Dict:
        packet = super().encode()
        packet["asteroids"] = self.asteroids
        return packet

    @staticmethod
    def get_type() -> str:
        return "game_init"
