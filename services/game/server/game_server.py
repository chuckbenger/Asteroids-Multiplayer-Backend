from typing import Dict, Optional
from flask_socketio import Namespace, join_room, leave_room, emit

from common.domain.game import Game
from common.domain.player import Player
from common.domain.actions import GetGame, UpdateGame

from server.identity import IdentityManager, GameIdentity
from server.game_rooms import GameRooms
from server import GameRoomMessenger, GameMessage
from server.packets.packet import Packet
from server.packets import decode_packet


class WebSocketMessenger(GameRoomMessenger):

    def send_game_room(self, message: Packet, game_id: str) -> None:
        emit('data', message.encode(), room=game_id)

    def send_player(self, message: Packet) -> None:
        emit('data', message.encode())


class GameServerNamespace(Namespace):

    def __init__(self, namespace):
        Namespace.__init__(self, namespace)
        self.messenger = WebSocketMessenger()
        self.identity = IdentityManager()
        self.get_game = GetGame()
        self.update_game = UpdateGame()
        self.game_rooms = GameRooms(self.messenger)

    def on_join(self, data: Dict):
        player_id = data.get('player_id')
        game_id = data.get('game_id')

        identity = self.initialize_session(player_id, game_id)

        if not identity:
            print("Invalid Identity", data)
            return

        if self.validate_and_join_game(identity):
            join_room(identity.game_id)
            message = self._build_message(data)
            self.game_rooms.handle_message(message)
        else:
            print("Not a valid game", data)
            self.identity.reset_identity()

    def initialize_session(self, player_id, game_id) -> Optional[GameIdentity]:

        if not player_id or not game_id:
            return None

        self.identity.set_identity(player_id, game_id)

        return self.identity.get_identity()

    def validate_and_join_game(self, identity: GameIdentity) -> bool:
        if self.game_rooms.game_exists(identity.game_id):
            return True
        else:
            game = self.get_game.execute(identity.game_id)

            if game and game.active:
                player_ids = [p.player_id for p in game.players]
                self.game_rooms.create_game_room(game.game_id, player_ids)
                return True

        return False

    def on_leave(self, data: Dict):
        identity = self.identity.get_identity()
        message = self._build_message(data)

        if message and identity:
            leave_room(identity.game_id)
            self.identity.reset_identity()
            self.game_rooms.handle_message(message)
            self.check_game_end(identity.game_id)

    def check_game_end(self, game_id: str):
        game = self.game_rooms.get_game_room(game_id)

        if game and game.is_game_ended():
            self.end_game(game_id)

    def end_game(self, game_id: str):
        self.game_rooms.stop_game_room(game_id)
        game = self.get_game.execute(game_id)
        game.active = False
        self.update_game.execute(game)

    def on_data(self, data: Dict):
        message = self._build_message(data)

        if message:
            self.game_rooms.handle_message(message)

    def _build_message(self, m: Dict) -> Optional[GameMessage]:
        identity = self.identity.get_identity()
        if not identity:
            return None

        decoded = decode_packet(m)

        if decoded:
            return GameMessage(
                message=decoded,
                player_id=identity.player_id,
                game_id=identity.game_id
            )
        else:
            return None
