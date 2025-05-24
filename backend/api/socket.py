"""Socket.IO event handlers for the application."""

import socketio
from app.manager import AppManager
from events.data import JoinGameData, SubmitAnswerData
from events.events import ClientEvent


class SocketHandlers:
    """Socket.IO event handlers for the application."""
    SERVER: socketio.AsyncServer | None = None
    MANAGER: AppManager | None = None

    @staticmethod
    def setup(sio: socketio.AsyncServer, manager: AppManager):
        """Set up the socket handlers.

        Args:
            sio (socketio.AsyncServer): The SocketIO server instance.
            manager (AppManager): The application manager instance.
        """
        SocketHandlers.SERVER = sio
        SocketHandlers.MANAGER = manager
        SocketHandlers._setup()

    @staticmethod
    def _setup() -> None:
        """Set up all socket.io event handlers."""
        sio = SocketHandlers.SERVER
        sio.on(ClientEvent.JOIN_LOBBY)(SocketHandlers.handle_join_lobby)
        sio.on(ClientEvent.JOIN_GAME)(SocketHandlers.handle_join_game)
        sio.on(ClientEvent.SUBMIT_ANSWER)(SocketHandlers.handle_submit_answer)
        sio.on(ClientEvent.DISCONNECT)(SocketHandlers.handle_disconnect)

    @staticmethod
    async def handle_join_lobby(sid: str, _: dict):
        """Handles a player joining the lobby.

        Args:
            sid (str): The socket ID of the player.
            _ (dict): The data from the client.
        """
        print(f"[backend] {sid} joined lobby")
        await SocketHandlers.MANAGER.add_to_lobby(sid)

    @staticmethod
    async def handle_join_game(sid: str, data: dict):
        """Handles a player joining a game.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        event_data = JoinGameData.from_dict(data)
        print(f"[backend] {sid} joined game {event_data.game_id}")
        await SocketHandlers.MANAGER.join_game(sid, event_data)

    @staticmethod
    async def handle_submit_answer(sid: str, data: dict):
        """Handles a player submitting an answer.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        print(f"[backend] {sid} submitted answer {data}")
        event_data = SubmitAnswerData.from_dict(data)
        await SocketHandlers.MANAGER.submit_answer(sid, event_data)

    @staticmethod
    async def handle_disconnect(sid: str, _: dict):
        """Handles a player disconnecting from the server.

        Args:
            sid (str): The socket ID of the player.
        """
        print(f"[backend] {sid} disconnected")
        await SocketHandlers.MANAGER.remove_from_lobby(sid)
