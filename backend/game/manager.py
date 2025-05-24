"""Game manager for managing multiple game instances."""

import asyncio
import uuid

from events.data import NewGameData, SubmitAnswerData
from game.game import Game


class GameManager:
    """Manager for managing multiple game instances."""

    def __init__(self):
        self._games: dict[str, Game] = {}

    def new_game(self, players: list[str]) -> NewGameData:
        """Creates a new game.

        Args:
            players (list[str]): The players in the game.

        Returns:
            NewGameData: The new game data.
        """
        game_id = str(uuid.uuid4())
        game = Game(game_id, players)
        self._games[game_id] = game
        asyncio.create_task(game.start())
        return NewGameData(game_id)

    async def submit_answer(self, sid: str, data: SubmitAnswerData) -> None:
        """Submits an answer to the game.

        Args:
            sid (str): The socket id of the player.
            data (SubmitAnswerData): The data from the client.
        """
        self._games[data.game_id].submit_answer(sid, data.answer)
