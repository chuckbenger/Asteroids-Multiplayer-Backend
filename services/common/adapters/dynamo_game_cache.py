import boto3
import logging
from botocore.exceptions import ClientError
from typing import Optional, Dict
from common.domain.game_cache_interface import GameCacheInterface
from common.domain.game import Game, Player


class DynamoGameCacheAdapter(GameCacheInterface):

    def __init__(self, table_name: str) -> None:
        self.dynamo_db = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamo_db.Table(table_name)

    def add_new_game(self, game: Game) -> bool:
        self.table.put_item(
            Item=self._serialize_game(game)
        )
        return True

    def update_game(self, game: Game) -> bool:
        self.table.put_item(
            Item=self._serialize_game(game)
        )
        return True

    def get_game(self, game_id: str) -> Optional[Game]:
        try:
            response = self.table.get_item(Key={"GameID": game_id})
        except ClientError as e:
            logging.error(e.response)
            return None
        else:
            print("GOT BACK", response)
            item = response.get("Item")
            if item:
                return self._deserialize_game(item)
            return None

    def _serialize_game(self, game: Game) -> Dict:
        return {
            "GameID": game.game_id,
            "Players": [
                {"player_id": player.player_id, "player_name": player.name}
                for player in game.players
            ],
            "Created": game.created,
            "Active": game.active
        }

    def _deserialize_game(self, data: Dict) -> Game:
        game_id = data["GameID"]
        active = data["Active"]
        created = data["Created"]
        players = [Player(player['player_id'], player['player_name'], None)
                   for player in data["Players"]]

        return Game(game_id, players, active, created)
