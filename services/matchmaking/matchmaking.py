import logging
import time
from configure import MatchMakerConfig, get_configuration, configure_inject
from common.domain.actions.get_players_waiting import GetPlayersWaiting
from common.domain.actions.get_players import GetPlayers
from common.domain.actions.add_new_game import AddNewGame
from common.domain.player import Player
from common.domain.game import create_new_game, Game


class MatchMakerApp:
    def __init__(self, config: MatchMakerConfig):
        self.config = config
        self.get_players_waiting = GetPlayersWaiting()
        self.get_players = GetPlayers()
        self.add_new_game = AddNewGame()

    def start(self) -> None:
        while True:
            if self.can_setup_match():
                players = self.find_players_for_match()
                game = self.setup_match(players)
                logging.info(f"New Game {game}")
            else:
                logging.info("Not enough players in game queue")

            time.sleep(self.config.seconds_between_queue_scans)

    def can_setup_match(self) -> bool:
        return self.get_players_waiting.execute() >= self.config.players_per_game

    def find_players_for_match(self) -> [Player]:
        return self.get_players.execute(self.config.players_per_game)

    def setup_match(self, players: [Player]) -> Game:
        game = create_new_game(players)

        if self.add_new_game.execute(game):
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
