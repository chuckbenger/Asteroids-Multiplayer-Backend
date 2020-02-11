import random
from typing import Dict, List
from flask_socketio import emit

from server.packets.game_join import GameJoinPacket
from server.packets.game_left import GameLeftPacket
from server.packets.game_init import GameInitPacket
from server import GameRoomMessenger, GameMessage


class Asteroid:
    def __init__(self, x, y, angle, sides, size, velocity,
                 rotation_speed, lives):
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
            x=random.randint(0, 400),
            y=random.randint(0, 500),
            angle=random.randint(0, 0),
            sides=6,
            size=random.randint(1, 20),
            velocity=random.randint(1, 3),
            rotation_speed=random.randint(1, 3),
            lives=2
        )
        asteroids.append(asteroid)
    return asteroids


class GameRoom():
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.players: Dict = {}
        self.asteroids: List = [x.to_dict() for x in generate_asteroid_field()]
        self.score = 0
        self.level = 0

    def add_player(self, player_id: str) -> None:
        self.players[player_id] = player_id
        self._notify_player_joined(player_id)
        self._setup_new_player()

    def _notify_player_joined(self, new_player_id: str) -> None:
        self._send_room(GameJoinPacket(new_player_id, self.game_id).encode())

    def _setup_new_player(self) -> None:
        for player in self.players.keys():
            self._send_self(GameJoinPacket(player, self.game_id).encode())

    def remove_player(self, player_id: str) -> None:
        del self.players[player_id]
        self._notify_player_left(player_id)

    def _notify_player_left(self, player_id: str):
        self._send_room(GameLeftPacket(player_id, self.game_id).encode())

    def initialize_game(self) -> None:
        self._send_room(GameInitPacket(self.asteroids).encode())

    def handle_message(self, message: GameMessage,
                       messenger: GameRoomMessenger) -> None:
        messenger.send_game_room(message)
