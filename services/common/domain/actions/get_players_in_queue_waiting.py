from common.domain.player import Player
from common.domain.game_queue_interface import GameQueueInterface
import inject


class GetPlayersInQueueWaiting:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self) -> int:
        return self.__queue.size()
