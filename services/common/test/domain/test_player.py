import pytest
import inject
from unittest.mock import Mock
from common.domain.game_queue_interface import GameQueueInterface
from common.domain.player import Player
from common.domain.actions.add_player_to_queue import AddPlayerToQueue
from common.domain.actions.get_players_in_queue import GetPlayersInQueue
from common.domain.actions.get_players_in_queue_waiting import GetPlayersInQueueWaiting


@pytest.fixture
def game_queue():
    return Mock()


@pytest.fixture
def injector(game_queue: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(GameQueueInterface, game_queue))


@pytest.fixture
def player() -> Player:
    return Player('chuckbenger')


class TestPlayer:

    def test_add_player(self, injector, game_queue, player):
        game_queue.push.return_value = True

        result = AddPlayerToQueue().execute(player)

        assert result == True
        game_queue.push.assert_called_once_with(player)

    def test_get_players(self, injector, game_queue, player):
        game_queue.pop.return_value = player

        result = GetPlayersInQueue().execute(1)

        assert result == player
        game_queue.pop.assert_called_once_with(1)

    def test_get_players_waiting(self, injector, game_queue, player):
        game_queue.size.return_value = 1

        result = GetPlayersInQueueWaiting().execute()

        assert result == 1
        game_queue.size.assert_called_once()
