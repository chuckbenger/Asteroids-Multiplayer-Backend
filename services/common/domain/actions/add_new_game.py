from common.domain.game import Game
from common.domain.cache_interface import GameCacheInterface
import inject


class AddNewGame:

    @inject.autoparams('cache')
    def __init__(self, cache: GameCacheInterface):
        self.__cache = cache

    def execute(self, game: Game) -> bool:
        return self.__cache.add_new_game(game)
