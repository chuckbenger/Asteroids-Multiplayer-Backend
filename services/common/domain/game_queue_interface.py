from abc import ABC, abstractmethod
from typing import List
from common.domain.game import Player


class GameQueueInterface(ABC):

    @abstractmethod
    def push(self, game: Player) -> bool:
        pass

    @abstractmethod
    def pop(self, max_size: int = 1) -> List[Player]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass
