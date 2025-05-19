"""Events that can be emitted by the server."""

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


class EventQueue:
    """A queue of events that can be emitted by the server."""

    _events = Queue[ServerEvent]()

    @staticmethod
    def put(event: ServerEvent) -> None:
        """Add an event to the queue.

        Args:
            event (ServerEvent): The event to add to the queue.
        """
        EventQueue._events.put(event)

    @staticmethod
    def get() -> ServerEvent:
        """Get an event from the queue.

        Returns:
            ServerEvent: The event from the queue.
        """
        return EventQueue._events.get()
