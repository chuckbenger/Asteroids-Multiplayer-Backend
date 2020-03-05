import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    player_id: str
    name: str
    game_id: Optional[str]


def create_player(name: str) -> Player:
    return Player(str(uuid.uuid4()), name, None)
