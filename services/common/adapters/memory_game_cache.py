from typing import Optional, Dict
from common.domain.game_cache_interface import GameCacheInterface
from common.domain.game import Game, Player


class MemoryGameCacheAdapter(GameCacheInterface):

    def __init__(self):
        self.games: Dict[str, Game] = {}

    def add_new_game(self, game: Game) -> bool:
        self.games[game.game_id] = game
        return True

    def update_game(self, game: Game) -> bool:
        self.games[game.game_id] = game
        return True

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.games.get(game_id)
