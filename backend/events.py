"""Events that can be emitted by the server."""

from asyncio import Queue
from enum import Enum

from data_models import EventData


class ClientEvent(str, Enum):
    """The events that can be emitted by the client."""

    JOIN_LOBBY = "join_lobby"
    JOIN_GAME = "join_game"
    SUBMIT_ANSWER = "submit_answer"
    DISCONNECT = "disconnect"


class ServerEvent(str, Enum):
    """The events that can be emitted by the server."""

    LOBBY_UPDATE = "lobby_update"
    NEW_GAME = "new_game"
    GAME_UPDATE = "game_update"


class EventQueue:
    """A queue of events that can be emitted by the server."""

    _events = Queue[tuple[ServerEvent, EventData]]()

    @staticmethod
    async def put(event: ServerEvent, data: EventData) -> None:
        """Add an event to the queue.

        Args:
            event (ServerEvent): The event to add to the queue.
            data (EventData): The data associated with the event.
        """
        await EventQueue._events.put((event, data))

    @staticmethod
    async def get() -> tuple[ServerEvent, EventData]:
        """Get an event from the queue.

        Returns:
            tuple[ServerEvent, EventData]: The event and data from the queue.
        """
        return await EventQueue._events.get()
