from typing import Dict, Union
from flask import session
from flask_socketio import Namespace, join_room, leave_room
from server.game_room import GameRoom


class GameServerNamespace(Namespace):

    def __init__(self, namespace):
        Namespace.__init__(self, namespace)
        self.game_rooms: Dict[str, GameRoom] = {}

    def on_join(self, message: Dict):
        game_id = message['game_id']
        player_id = message['player_id']

        game = self.get_game_room(game_id)
        if not game:
            game = self.create_game_room(game_id)

        game.add_player(player_id)
        join_room(game_id)
        game.initialize_game()
        session['game_id'] = game_id
        session['player_id'] = player_id

    def on_leave(self, message: Dict):
        game_id = session['game_id']
        player_id = session['player_id']
        game = self.get_game_room(game_id)

        if game:
            game.remove_player(player_id)
        leave_room(game_id)
        session['game_id'] = None
        session['player_id'] = None

    def on_data(self, message: Dict):
        game_id = session["game_id"]
        player_id = session["player_id"]

        if game_id and player_id:
            self.handle_game_message(message, game_id, player_id)

    def handle_game_message(self, message: Dict, game_id: str, player_id: str):
        game = self.get_game_room(game_id)
        if game:
            game.handle_message(message, player_id)

    def create_game_room(self, game_id: str) -> GameRoom:
        game_room = GameRoom(game_id)
        self.game_rooms[game_id] = game_room
        return game_room

    def get_game_room(self, game_id: str) -> Union[None, GameRoom]:
        return self.game_rooms.get(game_id)
