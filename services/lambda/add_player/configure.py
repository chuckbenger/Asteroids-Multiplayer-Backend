import inject
from common.adapters import SQSGameQueueAdapter
from common.domain import GameQueueInterface


def configure_inject(sqs_match_making_queue_name: str) -> None:

    def config(binder: inject.Binder) -> None:
        binder.bind(GameQueueInterface, SQSGameQueueAdapter(
            sqs_match_making_queue_name))

    inject.configure(config)
