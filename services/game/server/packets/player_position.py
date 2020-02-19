from typing import Dict
from server.packets.packet import Packet


class PlayerPositionPacket(Packet):

    def __init__(self, x: float, y: float, angle: float, player_id: str, thrusting: bool):
        self.x = x
        self.y = y
        self.angle = angle
        self.player_id = player_id
        self.thrusting = thrusting

    def encode(self) -> Dict:
        packet = super().encode()
        packet['player_id'] = self.player_id
        packet['x'] = self.x
        packet['y'] = self.y
        packet['angle'] = self.angle
        packet['thrusting'] = self.thrusting
        return packet

    @staticmethod
    def decode(data: Dict):
        return PlayerPositionPacket(
            x=data['x'],
            y=data['y'],
            angle=data['angle'],
            player_id=data['player_id'],
            thrusting=data['thrusting']
        )

    @staticmethod
    def get_type() -> str:
        return "player_update"
