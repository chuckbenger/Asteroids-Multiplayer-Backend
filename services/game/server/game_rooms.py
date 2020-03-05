

from typing import Dict, List, Optional

from common.domain.game import Game
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

    def create_game_room(self, game_id: str, player_ids: List[str]) -> GameRoom:
        if self.game_exists(game_id):
            return self.get_game_room(game_id)
        else:
            new_game = GameRoom(game_id, player_ids, self.messenger)
            self.game_rooms[game_id] = new_game
            return new_game

    def game_exists(self, game_id: str) -> bool:
        return self.get_game_room(game_id) is not None

    def get_game_room(self, game_id: str) -> Optional[GameRoom]:
        return self.game_rooms.get(game_id)

    def stop_game_room(self, game_id: str) -> None:
        print("ENDING GAME", game_id)
        del self.game_rooms[game_id]