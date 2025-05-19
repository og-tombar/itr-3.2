"""A simple in-memory lobby."""

from threading import Timer

from events import EventQueue, ServerEvent


class Lobby:
    """A simple in-memory lobby."""

    ROOM = 'lobby'
    TIMEOUT_SECONDS = 5
    MIN_PLAYERS = 4

    def __init__(self):
        self._players = set[str]()
        self._timer: Timer | None = None

    def add_player(self, sid: str) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        self._players.add(sid)
        if not self._timer:
            self._start_timer()
        should_game_start = len(self._players) >= Lobby.MIN_PLAYERS
        if should_game_start:
            self._on_start_game()

    def remove_player(self, sid: str) -> None:
        """Removes a player from the lobby.

        Args:
            sid (str): The sid of the player to remove.
        """
        self._players.remove(sid)
        if not self._players:
            self._stop_timer()

    def get_players(self) -> list[str]:
        """Gets the players in the lobby.

        Returns:
            list[str]: The players in the lobby.
        """
        return list(self._players).copy()

    def clear(self) -> None:
        """Clears the lobby."""
        self._players.clear()
        self._stop_timer()

    def _start_timer(self) -> None:
        """Starts the timer."""
        if self._timer:
            self._timer.cancel()
        self._timer = Timer(Lobby.TIMEOUT_SECONDS, self._on_timeout)
        self._timer.start()

    def _stop_timer(self) -> None:
        """Stops the timer."""
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _on_timeout(self) -> None:
        """Called when the timer runs out."""
        if self._players:
            self._on_start_game()
        else:
            self._start_timer()

    def _on_start_game(self) -> None:
        """Called when the game starts."""
        self._stop_timer()
        EventQueue.put(ServerEvent.NEW_GAME)
