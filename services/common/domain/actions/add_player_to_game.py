import inject
from common.domain.player import Player
from common.domain.player_cache_interface import PlayerCacheInterface


class AddPlayerToGame:

    @inject.autoparams('cache')
    def __init__(self, cache: PlayerCacheInterface):
        self.__cache = cache

    def execute(self, player: Player) -> bool:
        return self.__cache.add_player(player)
