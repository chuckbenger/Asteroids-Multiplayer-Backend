import inject
from typing import Optional
from common.domain.game import Game
from common.domain.game_cache_interface import GameCacheInterface


class GetGame:

    @inject.autoparams('cache')
    def __init__(self, cache: GameCacheInterface):
        self.__cache = cache

    def execute(self, game_id: str) -> Optional[Game]:
        return self.__cache.get_game(game_id)
