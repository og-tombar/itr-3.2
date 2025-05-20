"""Data models for the backend."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EventData(ABC):
    """The data associated with an event."""

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> "EventData":
        """Convert the data to a dictionary."""


@dataclass
class LobbyUpdateData(EventData):
    """The data associated with a lobby update event."""
    players: list[str]
    time_remaining: int
    should_start_game: bool

    @staticmethod
    def from_dict(d: dict) -> "LobbyUpdateData":
        """Convert the data to a dictionary."""
        return LobbyUpdateData(d["players"], d["time_remaining"], d["should_start_game"])


@dataclass
class JoinGameData(EventData):
    """The data associated with a join game event."""
    game_id: str

    @staticmethod
    def from_dict(d: dict) -> "JoinGameData":
        """Convert the data to a dictionary."""
        return JoinGameData(d["game_id"])


@dataclass
class Game:
    """The data for a game state."""
    id: str
    players: list[str]
