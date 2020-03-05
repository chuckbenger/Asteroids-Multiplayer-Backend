from flask import session
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GameIdentity:
    player_id: str
    game_id: str


class IdentityManager:

    def set_identity(self, player_id: Optional[str], game_id: Optional[str]) -> None:
        session['player_id'] = player_id
        session['game_id'] = game_id

    def get_identity(self) -> Optional[GameIdentity]:
        player_id = session.get('player_id')
        game_id = session.get('game_id')

        if player_id is None or game_id is None:
            return None

        return GameIdentity(
            player_id=player_id,
            game_id=game_id
        )

    def reset_identity(self) -> None:
        session['player_id'] = None
        session['game_id'] = None
