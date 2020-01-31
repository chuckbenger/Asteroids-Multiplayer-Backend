import pytest
import boto3
import os
from moto import mock_sqs
from common.domain.player import Player


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def game_queue(aws_credentials):
    with mock_sqs():
        from common.adapters.sqs import SQSGameQueueAdapter

        sqs = boto3.resource('sqs',  'ca-central-1')
        sqs.create_queue(QueueName='TestQueue')
        yield SQSGameQueueAdapter("TestQueue")


@pytest.fixture(scope='function')
def test_player():
    return Player('chuckbenger')


@pytest.fixture(autouse=True)
def empty_game_queue(game_queue):
    game_queue.purge()


class TestSQSAdapter:

    def test_can_add_player_to_queue(self, game_queue, test_player):
        game_queue.push(test_player)
        assert game_queue.size() > 0

    def test_can_remove_player_from_queue(self, game_queue, test_player):
        game_queue.push(test_player)
        players = game_queue.pop(1)
        assert len(players) == 1
        assert players[0] == test_player

    def test_can_add_multiple_players_to_queue(self, game_queue):
        players = [
            Player('chuckbenger1'),
            Player('chuckbenger2'),
            Player('chuckbenger3'),
            Player('chuckbenger4')
        ]
        for player in players:
            game_queue.push(player)

        assert game_queue.size() == 4

        popped_players = game_queue.pop(4)

        for player in players:
            assert player in popped_players

    def test_empty_pop(self, game_queue):
        players = game_queue.pop(1)
        assert len(players) == 0
   