"""Manages the game state."""

import uuid

from data_models import Game


class GameManager:
    """Manages multiple game instances."""

    def __init__(self):
        self.games: dict[str, Game] = {}

    def new_game(self, players: list[str]) -> Game:
        """Creates a new game.

        Args:
            players (list[str]): The players in the game.

        Returns:
            Game: The new game.
        """
        game = Game(str(uuid.uuid4()), players)
        self.games[game.id] = game
        return game
