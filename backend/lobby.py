"""A simple in-memory lobby."""

from events import EventQueue, LobbyUpdateData, ServerEvent
from interval_timer import IntervalTimer
from interval_timer.interval import Interval


class Lobby:
    """A simple in-memory lobby."""

    ROOM = 'lobby'
    TIMEOUT_SECONDS = 30
    MAX_PLAYERS = 4

    def __init__(self):
        self._players = set[str]()
        self._is_timer_active = False

    def add_player(self, sid: str) -> None:
        """Adds a player to the lobby.

        Args:
            sid (str): The sid of the player to add.
        """
        self._players.add(sid)
        if not self._is_timer_active:
            self._start_timer()

    def remove_player(self, sid: str) -> None:
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

    def _start_timer(self) -> None:
        """Starts the timer."""
        self._is_timer_active = True
        while self._is_timer_active:
            for interval in IntervalTimer(1, stop=Lobby.TIMEOUT_SECONDS):
                if not self._is_timer_active:
                    return
                self._tick(interval)

    def _tick(self, interval: Interval) -> None:
        """Called when the timer ticks."""
        time_remaining = Lobby.TIMEOUT_SECONDS - interval.time - 1
        should_start_game = (
            len(self._players) >= Lobby.MAX_PLAYERS
            or (time_remaining <= 0 < len(self._players))
        )
        data = LobbyUpdateData(
            players=list(self._players),
            time_remaining=time_remaining,
            should_start_game=should_start_game,
        )
        EventQueue.put(ServerEvent.LOBBY_UPDATE, data)
        if should_start_game:
            self._is_timer_active = False
