import boto3
import logging
from common.domain.player import Player
from common.domain.queue_interface import GameQueueInterface


class SQSGameQueueAdapter(GameQueueInterface):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.sqs = boto3.resource('sqs')
        self.client = boto3.client('sqs')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def push(self, player: Player) -> bool:
        response = self.queue.send_message(
            MessageAttributes={
                "user_id": {
                    "DataType": "String",
                    "StringValue": player.user_id
                }
            },
            MessageBody="Match Making"
        )
        return response and response['MessageId']

    def pop(self, max_size: int = 1) -> [Player]:
        messages = self.queue.receive_messages(
            MessageAttributeNames=['user_id'],
            MaxNumberOfMessages=max_size,
        )
        players = set()

        for message in messages:
            if message.message_attributes:
                user_id = message.message_attributes.get(
                    'user_id').get('StringValue')
                player = Player(user_id)
                players.add(player)

            message.delete()

        return list(players)

    def size(self) -> int:
        results = self.client.get_queue_attributes(
            QueueUrl=self.queue.url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        if results:
            return int(results['Attributes']['ApproximateNumberOfMessages'])
        else:
            return 0

    def purge(self) -> None:
        self.queue.purge()
