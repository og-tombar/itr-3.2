"""Data classes for events."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from player.player import Player


@dataclass
class EventData(ABC):
    """The data associated with an event."""


@dataclass
class ClientEventData(EventData):
    """The data associated with a client event."""

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> "ClientEventData":
        """Create a new client event data object from a dictionary."""


@dataclass
class NewPlayerData(ClientEventData):
    """The data associated with a new player event."""
    name: str

    @staticmethod
    def from_dict(d: dict) -> "NewPlayerData":
        """Create a new new player data object from a dictionary."""
        return NewPlayerData(d["name"])


@dataclass
class JoinGameData(ClientEventData):
    """The data associated with a join game event."""
    game_id: str

    @staticmethod
    def from_dict(d: dict) -> "JoinGameData":
        """Create a new join game data object from a dictionary."""
        return JoinGameData(d["game_id"])


@dataclass
class SubmitAnswerData(ClientEventData):
    """The data associated with a submit answer event."""
    answer: int

    @staticmethod
    def from_dict(d: dict) -> "SubmitAnswerData":
        """Create a new submit answer data object from a dictionary."""
        return SubmitAnswerData(d["answer"])


@dataclass
class PlayerInfoData(EventData):
    """The data associated with a player info event."""
    id: str
    name: str


@dataclass
class LobbyUpdateData(EventData):
    """The data associated with a lobby update event."""
    players: list[str]
    time_remaining: int
    should_start_game: bool


@dataclass
class NewGameData(EventData):
    """The data associated with a new game event."""
    id: str


@dataclass
class GameUpdateData(EventData):
    """The data associated with a game update event."""
    id: str
    phase: str
    players: dict[str, Player] = field(default_factory=dict)
    question_text: str = ""
    question_options: list[str] = field(default_factory=list)
    correct_answer: int = -1
    time_remaining: int = 0

    def to_dict(self) -> dict:
        """Convert the game update data to a dictionary.

        Returns:
            dict: The game update data as a dictionary.
        """
        d = self.__dict__.copy()
        d["players"] = {sid: p.__dict__ for sid, p in self.players.items()}
        return d


@dataclass
class MessageData(EventData):
    """The data associated with a message event."""
    id: str
    sender_id: str
    username: str
    message: str
    timestamp: str = datetime.now().isoformat()

    @staticmethod
    def from_dict(d: dict) -> "MessageData":
        """Create a new message data object from a dictionary."""
        return MessageData(d["id"], d["sender_id"], d["username"], d["message"], d["timestamp"])
