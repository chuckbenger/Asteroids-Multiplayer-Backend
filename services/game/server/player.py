

class Player:

    def __init__(self, player_id: str, player_name: str):
        self.player_id = player_id
        self.player_name = player_name
        self._score = 0

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value) -> None:
        self._score = value

    def get_name(self) -> str:
        return self.player_name

    def get_id(self) -> str:
        return self.player_id
