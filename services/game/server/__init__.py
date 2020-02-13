
from abc import ABC, abstractmethod
from typing import Dict, Union
from dataclasses import dataclass

from server.packets.packet import Packet


@dataclass(frozen=True)
class GameMessage:
    message: Packet
    player_id: str
    game_id: str


class GameRoomMessenger(ABC):

    @abstractmethod
    def send_game_room(self, message: Packet, game_id: str) -> None:
        pass

    @abstractmethod
    def send_player(self, message: Packet) -> None:
        pass

