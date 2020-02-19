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
from server.packets.player_died import PlayerDiedPacket
from server.packets.player_respawn import PlayerRespawnPacket
from server.asteroid import Asteroid, generate_asteroid_field
from server.player import Player
from server import GameRoomMessenger, GameMessage


class GameRoom():
    def __init__(self, game_id: str, messenger: GameRoomMessenger):
        self.game_id = game_id
        self.messenger = messenger
        self.players: Dict[str, Player] = {}
        self.asteroids: Dict[str, Asteroid] = {}
        self.score = 0
        self.level = 1

    def send_game_room(self, packet: Packet) -> None:
        self.messenger.send_game_room(packet, self.game_id)

    def send_player(self, packet: Packet) -> None:
        self.messenger.send_player(packet)

    def next_level(self) -> None:
        self.level = + 1
        self.initialize_level()

    def initialize_level(self) -> None:
        self.generate_asteroid_field()
        self.send_game_room(GameInitPacket(list(self.asteroids.values())))

    def generate_asteroid_field(self) -> None:
        asteroids = generate_asteroid_field(random.randint(5, 10 + self.level))
        self.asteroids = {a.id: a for a in asteroids}

    def handle_message(self, message: GameMessage) -> None:

        if message:
            packet = message.message
            if isinstance(packet, PlayerPositionPacket):
                self._handle_player_position(packet)
            elif isinstance(packet, PlayerBlasterPacket):
                self._handle_player_blaster_packet(packet)
            elif isinstance(packet, AsteroidKilledPacket):
                self._handle_asteroid_killed_packet(packet, message.player_id)
            elif isinstance(packet, GameJoinPacket):
                self._handle_game_join_packet(packet)
            elif isinstance(packet, GameLeftPacket):
                self._handle_game_left_packet(packet)
            elif isinstance(packet, PlayerDiedPacket):
                self.send_game_room(packet)
            elif isinstance(packet, PlayerRespawnPacket):
                self.send_game_room(packet)

    def _handle_player_position(self, packet: PlayerPositionPacket) -> None:
        self.send_game_room(packet)

    def _handle_player_blaster_packet(self, packet: PlayerBlasterPacket) -> None:
        self.send_game_room(packet)

    def _handle_asteroid_killed_packet(self, packet: AsteroidKilledPacket, player_id: str) -> None:
        self.send_game_room(packet)

        player = self.players[player_id]
        player.score += 100
        print(player.score)

        del self.asteroids[packet.asteroid_id]
        if len(self.asteroids.keys()) == 0:
            self.next_level()

    def _handle_game_join_packet(self, packet: GameJoinPacket) -> None:
        self.send_game_room(packet)
        self.send_player(GameInitPacket(list(self.asteroids.values())))

        for player_id, player in self.players.items():
            self.send_player(GameJoinPacket(
                player_id, self.game_id, player.get_name()))

        player = Player(packet.player_id, packet.player_name)
        
        self.players[packet.player_id] = player
        print(len(self.players), packet)

    def _handle_game_left_packet(self, packet: GameLeftPacket) -> None:
        self.send_game_room(packet)
