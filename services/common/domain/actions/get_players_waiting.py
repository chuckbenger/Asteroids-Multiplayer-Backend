from common.domain.player import Player
from common.domain.queue_interface import GameQueueInterface
import inject


class GetPlayersWaiting:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self) -> int:
        return self.__queue.size()
