"""Game manager for managing multiple game instances."""

import asyncio
import uuid

from events.data import NewGameData
from game.game import Game
from player.player import BotLevel, Player, PowerUp


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

    def set_bot_level(self, game_id: str, level: BotLevel) -> None:
        """Sets the bot level for a game.

        Args:
            game_id (str): The id of the game.
            level (BotLevel): The level of the bot.
        """
        game = self._games.get(game_id)
        if game:
            game.set_bot_level(level)

    def submit_answer(self, player: Player, answer: int) -> None:
        """Submits an answer for a player.

        Args:
            player (Player): The player who submitted the answer.
            answer (int): The answer submitted by the player.
        """
        game = self._games.get(player.room)
        if game:
            game.submit_answer(player, answer)

    async def use_powerup(self, player: Player, powerup: PowerUp) -> None:
        """Uses a powerup for the player.

        Args:
            player (Player): The player who used the powerup.
            powerup (PowerUp): The powerup used by the player.
        """
        game = self._games.get(player.room)
        if game:
            await game.use_powerup(player, powerup)

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
