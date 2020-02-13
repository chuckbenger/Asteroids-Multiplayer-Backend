from dataclasses import dataclass
from typing import Dict, Union, Optional
from flask import session
from flask_socketio import Namespace, join_room, leave_room, emit

from server.game_rooms import GameRooms
from server import GameRoomMessenger, GameMessage
from server.packets.packet import Packet
from server.packets import decode_packet


class WebSocketMessenger(GameRoomMessenger):

    def send_game_room(self, message: Packet, game_id: str) -> None:
        emit('data', message.encode(), room=game_id)

    def send_player(self, message: Packet) -> None:
        emit('data', message.encode())


@dataclass(frozen=True)
class GameIdentity:
    player_id: str
    game_id: str


class GameServerNamespace(Namespace):

    def __init__(self, namespace):
        Namespace.__init__(self, namespace)
        self.messenger = WebSocketMessenger()
        self.game_rooms = GameRooms(self.messenger)

    def on_join(self, data: Dict):
        identity = GameIdentity(data['player_id'], data['game_id'])
        self._save_identity(identity)

        if not self.game_rooms.game_exists(identity.game_id):
            self.game_rooms.create_game_room(identity.game_id)

        join_room(identity.game_id)

        message = self._build_message(data)
        self.game_rooms.handle_message(message)

    def on_leave(self, data: Dict):
        identity = self._get_identity()
        message = self._build_message(data)

        if message and identity:
            leave_room(identity.game_id)
            self._clear_identity()
            self.game_rooms.handle_message(message)

    def on_data(self, data: Dict):
        message = self._build_message(data)

        if message:
            self.game_rooms.handle_message(message)

    def _build_message(self, m: Dict) -> Optional[GameMessage]:
        identity = self._get_identity()
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

    def _get_identity(self) -> Optional[GameIdentity]:
        if session['player_id'] is None or session['game_id'] is None:
            return None

        return GameIdentity(
            player_id=session['player_id'],
            game_id=session['game_id']
        )

    def _save_identity(self, identity: GameIdentity) -> None:
        session['game_id'] = identity.game_id
        session['player_id'] = identity.player_id

    def _clear_identity(self) -> None:
        session['game_id'] = None
        session['player_id'] = None
