import json
import os
from dataclasses import dataclass
from typing import Dict, Optional
from common.domain.actions import GetPlayer
from configure import configure_inject

configure_inject(os.environ['PLAYER_DYNAMO_TABLE_NAME'])


@dataclass
class Data:
    player_id: str


def execute(event, context):

    data = parse_parameters(event)

    if data:
        player = GetPlayer().execute(data.player_id)

        if player:
            return success_response(player.game_id)

    return error_response()


def parse_parameters(event) -> Optional[Data]:
    parameters = event.get('pathParameters')
    if parameters:
        player_id = parameters.get('player_id')

        if player_id:
            return Data(player_id)

    return None


def success_response(game_id: str) -> Dict:
    return {
        "statusCode": "200",
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Game found",
            "game_id": game_id
        }),
    }


def error_response() -> Dict:
    return {
        "statusCode": "400",
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": "Could not find game"}),
    }
