"""Event queue and management for the application."""

from asyncio import Queue
from enum import Enum

from events.data import EventData


class ClientEvent(str, Enum):
    """The events that can be emitted by the client."""
    GET_PLAYER = "get_player"
    NEW_PLAYER = "new_player"
    JOIN_LOBBY = "join_lobby"
    JOIN_GAME = "join_game"
    SELECT_CATEGORY = "select_category"
    SUBMIT_ANSWER = "submit_answer"
    DISCONNECT = "disconnect"
    MESSAGE = "client_message"


class ServerEvent(str, Enum):
    """The events that can be emitted by the server."""
    PLAYER_INFO = "player_info"
    PLAYER_REGISTERED = "player_registered"
    LOBBY_UPDATE = "lobby_update"
    NEW_GAME = "new_game"
    GAME_UPDATE = "game_update"
    MESSAGE = "server_message"


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
