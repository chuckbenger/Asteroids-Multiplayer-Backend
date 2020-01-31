from dataclasses import dataclass
from common.domain.player import Player
from typing import Union
import uuid


@dataclass(frozen=False)
class Game:
    game_id: str
    players: [Player]

    def to_json(self) -> {}:
        return {
            "game_id": self.game_id,
            "players": [player.user_id for player in self.players]
        }

    @staticmethod
    def from_json(data: dict):
        game_id = data['game_id']
        players = data['players']

        return Game(game_id, players)
        


def create_new_game(players) -> Game:
    return Game(str(uuid.uuid4()), players)
