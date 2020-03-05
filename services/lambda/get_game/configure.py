import inject
from common.adapters import DynamoPlayerCacheAdapter
from common.domain import PlayerCacheInterface


def configure_inject(player_table_name: str) -> None:

    def config(binder: inject.Binder) -> None:
        binder.bind(PlayerCacheInterface, DynamoPlayerCacheAdapter(
            player_table_name))

    inject.configure(config)
