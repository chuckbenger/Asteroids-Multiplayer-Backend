from common.domain.player import Player
from common.domain.queue_interface import GameQueueInterface
import inject


class GetPlayers:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self, max_size: int) -> [Player]:
        return self.__queue.pop(max_size)
