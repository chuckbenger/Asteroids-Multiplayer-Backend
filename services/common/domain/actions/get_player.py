import inject
from typing import Optional
from common.domain.player import Player
from common.domain import PlayerCacheInterface


class GetPlayer:

    @inject.autoparams('cache')
    def __init__(self, cache: PlayerCacheInterface):
        self.__cache = cache

    def execute(self, player_id: str) -> Optional[Player]:
        return self.__cache.get_player(player_id)
