import random
from typing import Dict, List
from flask_socketio import emit

from server.packets.packet import Packet
from server.packets.game_join import GameJoinPacket
from server.packets.game_left import GameLeftPacket
from server.packets.game_init import GameInitPacket
from server.packets.player_position import PlayerPositionPacket
from server.packets.player_blaster import PlayerBlasterPacket
from server.packets.asteroid_killed import AsteroidKilledPacket
from server import GameRoomMessenger, GameMessage


class Asteroid:
    def __init__(self, id, x, y, angle, sides, size, velocity,
                 rotation_speed, lives):
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.sides = sides
        self.size = size
        self.velocity = velocity
        self.rotiation_speed = rotation_speed
        self.lives = lives

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "sides": self.sides,
            "size": self.size,
            "velocity": self.velocity,
            "rotation_speed": self.rotiation_speed,
            "lives": self.lives
        }


def generate_asteroid_field() -> List[Asteroid]:
    asteroids = []
    for i in range(1):
        asteroid = Asteroid(
            id=str(random.randint(1, 999)),
            x=random.randint(0, 400),
            y=random.randint(0, 500),
            angle=random.randint(0, 0),
            sides=6,
            size=random.randint(20, 40),
            velocity=random.randint(1, 3),
            rotation_speed=random.randint(1, 3),
            lives=2
        )
        asteroids.append(asteroid)
    return asteroids


class GameRoom():
    def __init__(self, game_id: str, messenger: GameRoomMessenger):
        self.game_id = game_id
        self.messenger = messenger
        self.players: Dict = {}
        self.asteroids: List = [x.to_dict() for x in generate_asteroid_field()]
        self.score = 0
        self.level = 0

    def send_game_room(self, packet: Packet) -> None:
        self.messenger.send_game_room(packet, self.game_id)

    def send_player(self, packet: Packet) -> None:
        self.messenger.send_player(packet)

    def handle_message(self, message: GameMessage) -> None:

        if message:
            packet = message.message
            if isinstance(packet, PlayerPositionPacket):
                self._handle_player_position(packet)
            elif isinstance(packet, PlayerBlasterPacket):
                self._handle_player_blaster_packet(packet)
            elif isinstance(packet, AsteroidKilledPacket):
                self._handle_asteroid_killed_packet(packet)
            elif isinstance(packet, GameJoinPacket):
                self._handle_game_join_packet(packet)
            elif isinstance(packet, GameLeftPacket):
                self._handle_game_left_packet(packet)

    def _handle_player_position(self, packet: PlayerPositionPacket) -> None:
        self.send_game_room(packet)

    def _handle_player_blaster_packet(self, packet: PlayerBlasterPacket) -> None:
        self.send_game_room(packet)

    def _handle_asteroid_killed_packet(self, packet: AsteroidKilledPacket) -> None:
        self.send_game_room(packet)

    def _handle_game_join_packet(self, packet: GameJoinPacket) -> None:
        self.send_game_room(packet)
        self.send_player(GameInitPacket(self.asteroids))
        for player_id, _ in self.players.items():
            self.send_player(GameJoinPacket(player_id, self.game_id))

        self.players[packet.player_id] = True

    def _handle_game_left_packet(self, packet: GameLeftPacket) -> None:
        self.send_game_room(packet)
