from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    user_id: str
