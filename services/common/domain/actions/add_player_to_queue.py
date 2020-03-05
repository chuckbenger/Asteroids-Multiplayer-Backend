from common.domain.player import Player
from common.domain.game_queue_interface import GameQueueInterface
import inject


class AddPlayerToQueue:

    @inject.autoparams('queue')
    def __init__(self, queue: GameQueueInterface):
        self.__queue = queue

    def execute(self, player: Player) -> bool:
        return self.__queue.push(player)
