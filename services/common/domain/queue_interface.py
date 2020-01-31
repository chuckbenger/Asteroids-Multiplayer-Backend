from abc import ABC, abstractmethod
from common.domain.player import Player

class GameQueueInterface(ABC):

    @abstractmethod
    def push(self, player: Player) -> bool:
        pass

    @abstractmethod
    def pop(self, max_size: int = 1) -> [Player]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass
