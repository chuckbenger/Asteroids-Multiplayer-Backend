
from abc import ABC, abstractmethod
from typing import Dict, Union
from dataclasses import dataclass

from server.packets.packet import Packet


@dataclass(frozen=True)
class GameMessage:
    message: Union[Dict, Packet]
    player_id: str
    game_id: str


class GameRoomMessenger(ABC):

    @abstractmethod
    def send_game_room(self, message: GameMessage) -> None:
        pass

    @abstractmethod
    def send_player(self, message: GameMessage) -> None:
        pass
