"""Events that can be emitted by the server."""

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from queue import Queue


class ClientEvent(str, Enum):
    """The events that can be emitted by the client."""

    JOIN_LOBBY = "join_lobby"
    JOIN_GAME = "join_game"
    DISCONNECT = "disconnect"


class ServerEvent(str, Enum):
    """The events that can be emitted by the server."""

    LOBBY_UPDATE = "lobby_update"
    NEW_GAME = "new_game"
    NEW_QUESTION = "new_question"


@dataclass
class EventData(ABC):
    """The data associated with an event."""


@dataclass
class LobbyUpdateData(EventData):
    """The data associated with a lobby update event."""
    players: list[str]
    time_remaining: int
    should_start_game: bool


class EventQueue:
    """A queue of events that can be emitted by the server."""

    _events = Queue[tuple[ServerEvent, EventData]]()

    @staticmethod
    def put(event: ServerEvent, data: EventData) -> None:
        """Add an event to the queue.

        Args:
            event (ServerEvent): The event to add to the queue.
            data (EventData): The data associated with the event.
        """
        EventQueue._events.put((event, data))

    @staticmethod
    def get() -> tuple[ServerEvent, EventData]:
        """Get an event from the queue.

        Returns:
            tuple[ServerEvent, EventData]: The event and data from the queue.
        """
        return EventQueue._events.get()
