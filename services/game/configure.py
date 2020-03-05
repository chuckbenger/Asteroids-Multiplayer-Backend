import os
import inject
from dataclasses import dataclass
from common.domain.game_cache_interface import GameCacheInterface
from common.domain.game import Game
from common.domain.player import Player
from common.adapters.memory_game_cache import MemoryGameCacheAdapter
from common.adapters import DynamoGameCacheAdapter


@dataclass(frozen=True)
class GameConfig:
    debug_mode: bool
    game_secret: str
    game_dynamo_table: str
    use_memory_cache: bool

    def __str__(self) -> str:
        return f"""
        === GameConfig ===
        debug_mode: {self.debug_mode}
        Game Dynamo Table: {self.game_dynamo_table}
        Use Memory Cache: {self.use_memory_cache}
        """


def get_configuration() -> GameConfig:
    return GameConfig(
        debug_mode=bool(os.environ["DEBUG"]),
        game_secret=str(os.environ['GAME_SECRET']),
        game_dynamo_table=str(os.environ['GAME_DYNAMO_TABLE']),
        use_memory_cache=False
    )


def configure_inject(c: GameConfig) -> None:

    print(c)

    def config(binder: inject.Binder) -> None:
        if c.use_memory_cache:
            instance = MemoryGameCacheAdapter()
            players = [
                Player('1', '1', None),
                Player('2', '2', None)
            ]
            instance.add_new_game(Game(123, players, True, 0))

            binder.bind(GameCacheInterface, instance)
        else:
            binder.bind(GameCacheInterface,
                        DynamoGameCacheAdapter(c.game_dynamo_table))

    inject.configure(config)
