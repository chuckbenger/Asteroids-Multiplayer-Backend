import json
from typing import Union
from common.domain.cache_interface import GameCacheInterface
from common.domain.game import Game
import redis


class RedisGameCacheAdapter(GameCacheInterface):

    def __init__(self, host: str, port: int, db: int) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.redis = redis.Redis(host, port, db)

    def add_new_game(self, game: Game) -> bool:
        key = str(game.game_id)
        value = json.dumps(game.to_json())
        return self.redis.set(key, value)

    def update_game(self, game: Game) -> bool:
        pass

    def get_game(self, game_id: str) -> Union[Game, None]:
        game = self.redis.get(game_id)
        print(game)
        return None

    def does_game_exist(self, game_id: str) -> bool:
        pass
