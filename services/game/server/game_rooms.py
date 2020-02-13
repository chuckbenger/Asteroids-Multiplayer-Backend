

from typing import Dict, Optional

from server.game_room import GameRoom
from server import GameRoomMessenger, GameMessage


class GameRooms:

    def __init__(self, messenger: GameRoomMessenger):
        self.game_rooms: Dict[str, GameRoom] = {}
        self.messenger = messenger

    def handle_message(self, message: GameMessage) -> None:
        game = self.get_game_room(message.game_id)

        if game:
            game.handle_message(message)

    def create_game_room(self, game_id: str) -> Optional[GameRoom]:
        if self.game_exists(game_id):
            return self.get_game_room(game_id)
        else:
            new_game = GameRoom(game_id, self.messenger)
            self.game_rooms[game_id] = new_game
            return new_game

    def game_exists(self, game_id: str) -> bool:
        return self.get_game_room(game_id) is not None

    def get_game_room(self, game_id: str) -> Optional[GameRoom]:
        return self.game_rooms.get(game_id)
