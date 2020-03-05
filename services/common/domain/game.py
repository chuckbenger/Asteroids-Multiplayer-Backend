import uuid
import time
from dataclasses import dataclass
from common.domain.player import Player
from typing import List


@dataclass
class Game:
    game_id: str
    players: List[Player]
    active: bool
    created: int


def create_new_game(players) -> Game:
    return Game(str(uuid.uuid4()), players, True, int(time.time()))
