"""A simple in-memory lobby."""

import asyncio

from data_models import LobbyUpdateData
from events import EventQueue, ServerEvent


class Lobby:
    """A simple in-memory lobby."""

    ROOM = 'lobby'
    TIMEOUT_SECONDS = 5
    MAX_PLAYERS = 4

    def __init__(self):
        self._players = set[str]()
        self._time_remaining = Lobby.TIMEOUT_SECONDS
        self._is_timer_active = False

    async def add_player(self, sid: str) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        self._players.add(sid)
        if not self._is_timer_active:
            asyncio.create_task(self._start_timer())

    async def remove_player(self, sid: str) -> None:
        """Removes a player from the lobby.

        Args:
            sid (str): The sid of the player to remove.
        """
        self._players.discard(sid)
        if not self._players:
            self._is_timer_active = False

    def get_players(self) -> list[str]:
        """Gets the players in the lobby.

        Returns:
            list[str]: The players in the lobby.
        """
        return list(self._players)

    def clear(self) -> None:
        """Clears the lobby."""
        self._is_timer_active = False
        self._players.clear()

    async def _start_timer(self) -> None:
        """Starts the timer."""
        self._time_remaining = Lobby.TIMEOUT_SECONDS
        self._is_timer_active = True
        while self._is_timer_active:
            await self._tick()
            await asyncio.sleep(1)
            self._time_remaining -= 1

    async def _tick(self) -> None:
        """Called when the timer ticks."""
        should_start_game = (
            len(self._players) >= Lobby.MAX_PLAYERS
            or (self._time_remaining <= 0 < len(self._players))
        )
        data = LobbyUpdateData(
            players=list(self._players),
            time_remaining=self._time_remaining,
            should_start_game=should_start_game,
        )
        await EventQueue.put(ServerEvent.LOBBY_UPDATE, data)
        if should_start_game:
            self._is_timer_active = False
