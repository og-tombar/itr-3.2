"""Lobby management service."""

import asyncio

from events.data import LobbyUpdateData
from events.events import EventQueue, ServerEvent
from player.player import Player


class Lobby:
    """Manages the game lobby."""

    ROOM = 'lobby'
    TIMEOUT_SECONDS = 5
    MAX_PLAYERS = 4

    def __init__(self):
        self._players: dict[str, Player] = {}
        self._time_remaining = self.TIMEOUT_SECONDS
        self._is_timer_active = False

    async def add_player(self, player: Player) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        self._players[player.sid] = player
        if not self._is_timer_active:
            asyncio.create_task(self._start_timer())

    def remove_player(self, player: Player) -> None:
        """Removes a player from the lobby.

        Args:
            sid (str): The sid of the player to remove.
        """
        self._players.pop(player.sid)
        if not self._players.values():
            self._is_timer_active = False

    def get_players(self) -> dict[str, Player]:
        """Gets the players in the lobby.

        Returns:
            dict[str, Player]: The players in the lobby.
        """
        return self._players.copy()

    def clear(self) -> None:
        """Clears the lobby."""
        self._is_timer_active = False
        self._players.clear()

    async def _start_timer(self) -> None:
        """Starts the timer."""
        self._time_remaining = self.TIMEOUT_SECONDS
        self._is_timer_active = True
        while self._is_timer_active:
            await self._tick()
            await asyncio.sleep(1)
            self._time_remaining -= 1

    async def _tick(self) -> None:
        """Called when the timer ticks."""
        should_start_game = (
            len(self._players) >= self.MAX_PLAYERS
            or (self._time_remaining <= 0 < len(self._players))
        )
        data = LobbyUpdateData(
            players=list(self._players.keys()),
            time_remaining=self._time_remaining,
            should_start_game=should_start_game,
        )
        await EventQueue.put(ServerEvent.LOBBY_UPDATE, data)
        if should_start_game:
            self._is_timer_active = False
