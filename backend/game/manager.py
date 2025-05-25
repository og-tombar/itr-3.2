"""Game manager for managing multiple game instances."""

import asyncio
import uuid

from events.data import NewGameData
from game.game import Game
from player.player import Player


class GameManager:
    """Manager for managing multiple game instances."""

    def __init__(self):
        self._games: dict[str, Game] = {}

    def new_game(self, players: dict[str, Player]) -> NewGameData:
        """Creates a new game.

        Args:
            players (dict[str, Player]): The players in the game.

        Returns:
            NewGameData: The new game data.
        """
        game_id = str(uuid.uuid4())
        game = Game(game_id, players)
        self._games[game_id] = game
        asyncio.create_task(game.start())
        return NewGameData(game_id)

    def remove_player(self, player: Player) -> None:
        """Removes a player from the game.

        Args:
            player (Player): The player to remove.
        """
        game = self._games.get(player.room)
        if game:
            game.remove_player(player)
            if game.is_empty():
                self._games.pop(player.room)
