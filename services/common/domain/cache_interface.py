from abc import ABC, abstractmethod
from typing import Union
from common.domain.game import Game


class GameCacheInterface(ABC):

    @abstractmethod
    def add_new_game(self, game: Game) -> bool:
        pass

    @abstractmethod
    def update_game(self, game: Game) -> bool:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Union[Game, None]:
        pass

    @abstractmethod
    def does_game_exist(self, game_id: str) -> bool:
        pass
