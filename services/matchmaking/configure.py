import os
import inject
from dataclasses import dataclass

from common.domain import GameCacheInterface, \
    GameQueueInterface, \
    PlayerCacheInterface
from common.adapters import SQSGameQueueAdapter, \
    DynamoGameCacheAdapter, \
    DynamoPlayerCacheAdapter


@dataclass(frozen=True)
class MatchMakerConfig:
    debug_mode: bool
    seconds_between_queue_scans: int
    max_games: int
    players_per_game: int
    match_queue_name: str
    game_table: str
    player_table: str

    def __str__(self) -> str:
        return f"""
        === MatchMakerConfig ===
        debug_mode: {self.debug_mode}
        seconds_between_queue_scans: {self.seconds_between_queue_scans}
        max_games: {self.max_games}
        players_per_game: {self.players_per_game}
        Match Queue Name: {self.match_queue_name}
        Game Table: {self.game_table}
        Player Table: {self.player_table}
        """


def get_configuration() -> MatchMakerConfig:
    return MatchMakerConfig(
        debug_mode=bool(os.environ["DEBUG"]),
        seconds_between_queue_scans=int(
            os.environ["SECONDS_BETWEEN_QUEUE_SCANS"]),
        max_games=bool(os.environ["MAX_GAMES"]),
        players_per_game=int(os.environ["PLAYERS_PER_GAME"]),
        match_queue_name=os.environ['MATCH_MAKING_QUEUE_NAME'],
        game_table=os.environ["GAME_TABLE"],
        player_table=os.environ["PLAYER_TABLE"]
    )


def configure_inject(c: MatchMakerConfig) -> None:
   
    def config(binder: inject.Binder) -> None:
        binder.bind(PlayerCacheInterface,
                    DynamoPlayerCacheAdapter(c.player_table))

        binder.bind(GameCacheInterface,
                    DynamoGameCacheAdapter(c.game_table))

        binder.bind(GameQueueInterface,
                    SQSGameQueueAdapter(c.match_queue_name))

    inject.configure(config)
