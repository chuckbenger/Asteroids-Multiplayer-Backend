
import uuid
import pytest
import inject
from unittest.mock import patch, Mock
from common.domain.game import Game, create_new_game
from common.domain.player import Player
from common.domain.cache_interface import GameCacheInterface
from common.domain.actions.add_new_game import AddNewGame


uuid_mock = Mock(return_value=str(
    uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')))

good_uuid = str(uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'))


@pytest.fixture
def game_cache():
    return Mock()


@pytest.fixture
def injector(game_cache):
    inject.clear_and_configure(lambda binder:
                               binder.bind(GameCacheInterface, game_cache))


@pytest.fixture
@patch(target='uuid.uuid4', new=uuid_mock)
def game_with_player():
    return create_new_game([Player('1234')])


class TestGame:

    def test_can_create_game(self, game_with_player):
        assert game_with_player.game_id == good_uuid
        assert len(game_with_player.players) == 1
        assert game_with_player.players[0].user_id == '1234'

    def test_to_json(self, game_with_player):
        assert game_with_player.to_json() == {
            'game_id': good_uuid,
            'players': ['1234']
        }

    def test_from_json(self):
        game = Game.from_json({
            'game_id': good_uuid,
            'players': []
        })

        assert game.game_id == good_uuid
        assert game.players == []

    def test_add_game_action(self, injector, game_cache, game_with_player):
        game_cache.add_new_game.return_value = True

        result = AddNewGame().execute(game_with_player)

        assert result == True
        game_cache.add_new_game.assert_called_once_with(game_with_player)
