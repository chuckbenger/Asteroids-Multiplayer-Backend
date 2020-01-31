# import pytest
# import os
# import boto3
# import inject
# from moto import mock_sqs
# from matchmaking.matchmaking import MatchMakerApp, MatchMakerConfig, get_configuration
# from common.domain.queue_interface import GameQueueInterface
# from common.domain.player import Player


# @pytest.fixture(scope='function')
# def aws_credentials():
#     """Mocked AWS Credentials for moto."""
#     os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
#     os.environ['AWS_SECURITY_TOKEN'] = 'testing'
#     os.environ['AWS_SESSION_TOKEN'] = 'testing'

# @pytest.fixture(scope='function')
# def game_queue(aws_credentials):
#     with mock_sqs():
#         from common.adapters.sqs import SQSGameQueueAdapter

#         sqs = boto3.resource('sqs',  'ca-central-1')
#         sqs.create_queue(QueueName='MyTestQueue')
#         yield SQSGameQueueAdapter("MyTestQueue")

# @pytest.fixture
# def configuration(game_queue) -> None:
#     return MatchMakerConfig(
#         debug_mode=False,
#         sleep_time_seconds=60,
#         game_queue=game_queue,
#         max_games=50,
#         players_per_game=2
#     )

# class TestMatchMaking:

#     def test_can_setup_match(self, configuration: MatchMakerConfig, game_queue: GameQueueInterface):
#         player = Player("test1")
#         player2 = Player("test2")
#         game_queue.push(player)
#         game_queue.push(player2)

#         app = MatchMakerApp(configuration)
#         assert app.can_setup_match()

#     def test_can_not_setup_match(self, configuration: MatchMakerConfig):
#         app = MatchMakerApp(configuration)
#         assert not app.can_setup_match()

#     def test_find_match_with_people_in_queue(self, configuration: MatchMakerConfig, game_queue: GameQueueInterface):
#         player = Player("test1")
#         player2 = Player("test2")
#         game_queue.push(player)
#         game_queue.push(player2)
        
#         app = MatchMakerApp(configuration)
#         players = app.find_players_for_match()

#         assert len(players) == 2

#     def test_find_match_with_no_people_in_queue(self, configuration: MatchMakerConfig):
#         app = MatchMakerApp(configuration)
#         players = app.find_players_for_match()

#         assert len(players) == 0
