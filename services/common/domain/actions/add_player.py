from common.domain.player import Player
from common.domain.queue_interface import GameQueueInterface
import inject


class AddPlayer:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self, player: Player) -> bool:
        return self.__queue.push(player)
