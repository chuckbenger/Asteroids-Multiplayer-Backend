import os
import inject
from dataclasses import dataclass
from common.domain.cache_interface import GameCacheInterface
from common.domain.queue_interface import GameQueueInterface
from common.adapters.redis_cache import RedisGameCacheAdapter


@dataclass(frozen=True)
class GameConfig:
    debug_mode: bool
    game_cache_redis_host: str
    game_cache_redis_port: int
    game_cache_redis_db: int
    game_secret: str

    def __str__(self) -> str:
        return f"""
        === GameConfig ===
        debug_mode: {self.debug_mode}
        Game Cache Host: {self.game_cache_redis_host}:
        Game Cache Port: {self.game_cache_redis_port}
        """


def get_configuration() -> GameConfig:
    return GameConfig(
        debug_mode=bool(os.environ["DEBUG"]),
        game_cache_redis_host=os.environ['GAME_CACHE_REDIS_HOST'],
        game_cache_redis_port=int(os.environ['GAME_CACHE_REDIS_PORT']),
        game_cache_redis_db=int(os.environ['GAME_CACHE_REDIS_DB']),
        game_secret=str(os.environ['GAME_SECRET'])
    )


def configure_inject(c: GameConfig) -> None:

    def config(binder: inject.Binder) -> None:
        binder.bind(GameCacheInterface, RedisGameCacheAdapter(
            c.game_cache_redis_host,
            c.game_cache_redis_port,
            c.game_cache_redis_db))

    inject.configure(config)
