import os
import inject
from dataclasses import dataclass
from common.domain.cache_interface import GameCacheInterface
from common.domain.queue_interface import GameQueueInterface
from common.adapters.sqs import SQSGameQueueAdapter
from common.adapters.redis_cache import RedisGameCacheAdapter


@dataclass(frozen=True)
class MatchMakerConfig:
    debug_mode: bool
    seconds_between_queue_scans: int
    max_games: int
    players_per_game: int
    game_cache_redis_host: str
    game_cache_redis_port: int
    game_cache_redis_db: int
    match_queue_name: str

    def __str__(self) -> str:
        return f"""
        === MatchMakerConfig ===
        debug_mode: {self.debug_mode}
        seconds_between_queue_scans: {self.seconds_between_queue_scans}
        max_games: {self.max_games}
        players_per_game: {self.players_per_game}
        Game Cache Host: {self.game_cache_redis_host}:{self.game_cache_redis_port}
        Match Queue Name: {self.match_queue_name}
        """


def get_configuration() -> MatchMakerConfig:
    return MatchMakerConfig(
        debug_mode=bool(os.environ["DEBUG"]),
        seconds_between_queue_scans=int(
            os.environ["SECONDS_BETWEEN_QUEUE_SCANS"]),
        max_games=bool(os.environ["MAX_GAMES"]),
        players_per_game=int(os.environ["PLAYERS_PER_GAME"]),
        game_cache_redis_host=os.environ['GAME_CACHE_REDIS_HOST'],
        game_cache_redis_port=int(os.environ['GAME_CACHE_REDIS_PORT']),
        game_cache_redis_db=int(os.environ['GAME_CACHE_REDIS_DB']),
        match_queue_name=os.environ['MATCH_MAKING_QUEUE_NAME']
    )


def configure_inject(c: MatchMakerConfig) -> None:

    def config(binder: inject.Binder) -> None:
        binder.bind(GameCacheInterface, RedisGameCacheAdapter(
            c.game_cache_redis_host,
            c.game_cache_redis_port,
            c.game_cache_redis_db))
        binder.bind(GameQueueInterface, SQSGameQueueAdapter(
            c.match_queue_name))

    inject.configure(config)
