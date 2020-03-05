from abc import ABC, abstractmethod
from typing import Optional
from common.domain.game import Player


class PlayerCacheInterface(ABC):

    @abstractmethod
    def add_player(self, player: Player) -> bool:
        pass

    @abstractmethod
    def update_player(self, game: Player) -> bool:
        pass

    @abstractmethod
    def get_player(self, player_id: str) -> Optional[Player]:
        pass
