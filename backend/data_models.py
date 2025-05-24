"""Data models for the backend."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class EventData(ABC):
    """The data associated with an event."""

############################################################
# Client event data
############################################################


@dataclass
class ClientEventData(EventData):
    """The data associated with a client event."""

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> "ClientEventData":
        """Convert the data to a dictionary."""


@dataclass
class JoinGameData(ClientEventData):
    """The data associated with a join game event."""
    game_id: str

    @staticmethod
    def from_dict(d: dict) -> "JoinGameData":
        """Convert the data to a dictionary."""
        return JoinGameData(d["game_id"])


@dataclass
class SubmitAnswerData(ClientEventData):
    """The data associated with a submit answer event."""
    game_id: str
    answer: int

    @staticmethod
    def from_dict(d: dict) -> "SubmitAnswerData":
        """Convert the data to a dictionary."""
        return SubmitAnswerData(d["game_id"], d["answer"])


############################################################
# Server event data
############################################################

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
    title: str
    scores: dict[str, int]
    question_text: str = ""
    question_options: list[str] = field(default_factory=list)
    answers: dict[str, int] = field(default_factory=dict)
    time_remaining: int = 0


############################################################
# Server data models
############################################################

@dataclass
class Player:
    """The data for a player."""
    id: str
    score: int = 0
    answer: int = -1


@dataclass
class Question:
    """The data for a question. Includes the correct answer (do not send to clients)."""
    id: str
    text: str
    options: list[str]
    correct_index: int
