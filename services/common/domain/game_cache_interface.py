from abc import ABC, abstractmethod
from typing import Optional
from common.domain.game import Game


class GameCacheInterface(ABC):

    @abstractmethod
    def add_new_game(self, game: Game) -> bool:
        pass

    @abstractmethod
    def update_game(self, game: Game) -> bool:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Optional[Game]:
        pass
