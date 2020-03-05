import inject
from common.domain.game import Game
from common.domain.game_cache_interface import GameCacheInterface


class UpdateGame:

    @inject.autoparams('cache')
    def __init__(self, cache: GameCacheInterface):
        self.__cache = cache

    def execute(self, game: Game) -> bool:
        return self.__cache.update_game(game)
