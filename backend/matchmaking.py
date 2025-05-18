"""Matchmaking module."""


import threading
import uuid
from dataclasses import dataclass


@dataclass
class GameState:
    """The data for a game state."""
    id: str
    players: list[str]


@dataclass
class LobbyState:
    """The data for a lobby update."""
    players: list[str]
    should_game_start: bool


class Lobby:
    """A simple in-memory lobby."""

    ROOM = 'lobby'
    TIMEOUT_SECONDS = 10
    MIN_PLAYERS = 2

    def __init__(self):
        self._players = set[str]()
        self._timer: threading.Timer | None = None

    def add_player(self, sid: str) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        self._players.add(sid)
        if self._players and not self._timer:
            self._start_timer()

    def get_state(self) -> LobbyState:
        """Gets the lobby state.

        Returns:
            LobbyState: The lobby state.
        """
        return LobbyState(
            players=list(self._players),
            should_game_start=len(self._players) >= Lobby.MIN_PLAYERS,
        )

    def start_game(self) -> GameState:
        """Starts the game.

        Returns:
            GameState: The state of the new game.
        """
        selected = list(self._players)
        self._players.clear()
        game_id = str(uuid.uuid4())
        return GameState(game_id, selected)

    def _start_timer(self) -> None:
        """Starts the timer."""
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(Lobby.TIMEOUT_SECONDS, self._on_timeout)
        self._timer.start()

    def _stop_timer(self) -> None:
        """Stops the timer."""
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _on_timeout(self) -> None:
        """Called when the timer runs out."""
        if self._players:
            self._stop_timer()
            self.start_game()
        else:
            self._start_timer()
