from common.domain.player import Player
from common.domain.game_queue_interface import GameQueueInterface
import inject


class GetPlayersInQueue:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self, max_size: int) -> [Player]:
        return self.__queue.pop(max_size)
