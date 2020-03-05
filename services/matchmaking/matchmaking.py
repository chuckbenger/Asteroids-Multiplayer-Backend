import logging
import time
from typing import List

from configure import MatchMakerConfig, get_configuration, configure_inject
from common.domain.player import Player
from common.domain.game import create_new_game, Game
from common.domain.actions import GetPlayersInQueueWaiting, \
    GetPlayersInQueue, \
    AddNewGame, \
    GetGame, \
    AddPlayerToGame


class MatchMakerApp:
    def __init__(self, config: MatchMakerConfig):
        self.config = config
        self.get_players_waiting = GetPlayersInQueueWaiting()
        self.get_players = GetPlayersInQueue()
        self.add_new_game = AddNewGame()
        self.add_player_to_game = AddPlayerToGame()

    def start(self) -> None:
        match: List[Player] = []
        while True:
            if self.can_setup_match():
                players = self.find_players_for_match(
                    self.config.players_per_game - len(match))

                match += players
                if len(match) >= self.config.players_per_game:
                    game = self.setup_match(match)
                    logging.info(f"New Game {game}")
                    match = []
            else:
                logging.info("Not enough players in game queue")

            time.sleep(self.config.seconds_between_queue_scans)

    def can_setup_match(self) -> bool:
        return self.get_players_waiting.execute() > 0

    def find_players_for_match(self, limit: int) -> List[Player]:
        return self.get_players.execute(limit)

    def setup_match(self, players: List[Player]) -> Game:
        game = create_new_game(players)

        if self.add_new_game.execute(game):

            for player in game.players:
                player.game_id = game.game_id
                self.add_player_to_game.execute(player)

            return game
        else:
            return None


if __name__ == '__main__':
    conf = get_configuration()

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting up match making service")
    logging.info(conf)
   
    configure_inject(conf)

    match_maker = MatchMakerApp(conf)
    match_maker.start()
