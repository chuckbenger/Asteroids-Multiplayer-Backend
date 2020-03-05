import json
import os
from dataclasses import dataclass
from typing import Dict, Optional

from common.domain.player import Player, create_player
from common.domain.actions import AddPlayerToQueue
from configure import configure_inject

configure_inject(os.environ['MATCH_MAKING_QUEUE_NAME'])


@dataclass
class Data:
    name: str


def execute(event, context):

    data = parse_body(event)

    if data:
        player = create_player(data.name)
        added_to_queue = AddPlayerToQueue().execute(player)

        if added_to_queue:
            return success_response(player.player_id)

    return error_response()


def parse_body(event) -> Optional[Data]:
    body = event.get('body')
    if body:
        json_data = json.loads(body)
        name = json_data.get('name')

        if name:
            return Data(name)

    return None


def success_response(player_id: str) -> Dict:
    return {
        "statusCode": "200",
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "message": "Added to Game Queue",
            "player_id": player_id
        }),
    }


def error_response() -> Dict:
    return {
        "statusCode": "400",
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": "Failed to join Game Queue"}),
    }
