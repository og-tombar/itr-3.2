"""Manages the game state."""

import uuid

from data_models import GameData
from questions import QuestionProvider


class GameManager:
    """Manages multiple game instances."""

    def __init__(self):
        self._games: dict[str, GameData] = {}
        self._provider = QuestionProvider()

    def new_game(self, players: list[str]) -> GameData:
        """Creates a new game.

        Args:
            players (list[str]): The players in the game.

        Returns:
            Game: The new game.
        """
        game = GameData(str(uuid.uuid4()), players)
        self._games[game.id] = game
        return game
