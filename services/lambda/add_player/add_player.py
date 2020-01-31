import json
import inject
import os
from common.domain.player import Player
from common.domain.actions.add_player import AddPlayer
from common.adapters.sqs import SQSGameQueueAdapter
from common.domain.queue_interface import GameQueueInterface


def configure_inject(sqs_match_making_queue_name: str) -> None:

    def config(binder: inject.Binder) -> None:
        binder.bind(GameQueueInterface, SQSGameQueueAdapter(
            sqs_match_making_queue_name))

    inject.configure(config)


configure_inject(os.getenv('MATCH_MAKING_QUEUE_NAME'))


@inject.autoparams("add_player")
def execute(event, context, add_player: AddPlayer):

    user_id = event['requestContext']['authorizer']['claims']['sub']

    if user_id:
        print(f"{user_id} being added to Game Queue")

        player = Player(user_id)
        was_added_to_queue = add_player.execute(player)

        if was_added_to_queue:
            return {
                "statusCode": "200",
                "body": json.dumps({"message": "Added to Game Queue"}),
            }

    return {
        "statusCode": "400",
        "body": json.dumps({"message": "Failed to join Game Queue"}),
    }
