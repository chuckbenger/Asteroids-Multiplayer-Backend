import boto3
import logging
from botocore.exceptions import ClientError
from typing import Optional, Dict
from common.domain.player_cache_interface import PlayerCacheInterface
from common.domain.player import Player


class DynamoPlayerCacheAdapter(PlayerCacheInterface):

    def __init__(self, table_name: str) -> None:
        self.dynamo_db = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamo_db.Table(table_name)

    def add_player(self, player: Player) -> bool:
        self.table.put_item(
            Item=self._serialize_player(player)
        )
        return True

    def update_player(self, game: Player) -> bool:
        self.table.put_item(
            Item=self._serialize_player(game)
        )
        return True

    def get_player(self, game_id: str) -> Optional[Player]:
        try:
            response = self.table.get_item(Key={"PlayerID": game_id})
        except ClientError as e:
            logging.error(e.response)
            return None
        else:
            item = response.get("Item")
            if item:
                return self._deserialize_player(item)
            else:
                return None

    def _serialize_player(self, player: Player) -> Dict:
        return {
            "PlayerID": player.player_id,
            "PlayerName": player.name,
            "GameID": player.game_id
        }

    def _deserialize_player(self, data: Dict) -> Player:
        player_id = data["PlayerID"]
        player_name = data["PlayerName"]
        game_id = data["GameID"]

        return Player(player_id, player_name, game_id)

