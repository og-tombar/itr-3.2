"""Socket.IO event handlers for the application."""

import socketio
from app.manager import AppManager
from events.data import (JoinGameData, MessageData, NewPlayerData,
                         SelectCategoryData, SetBotLevelData, SubmitAnswerData)
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
        SocketHandlers.SERVER.on(ClientEvent.GET_PLAYER)(
            SocketHandlers.handle_get_player)
        SocketHandlers.SERVER.on(ClientEvent.NEW_PLAYER)(
            SocketHandlers.handle_new_player)
        SocketHandlers.SERVER.on(ClientEvent.JOIN_LOBBY)(
            SocketHandlers.handle_join_lobby)
        SocketHandlers.SERVER.on(ClientEvent.JOIN_GAME)(
            SocketHandlers.handle_join_game)
        SocketHandlers.SERVER.on(ClientEvent.SET_BOT_LEVEL)(
            SocketHandlers.handle_set_bot_level)
        SocketHandlers.SERVER.on(ClientEvent.SELECT_CATEGORY)(
            SocketHandlers.handle_select_category)
        SocketHandlers.SERVER.on(ClientEvent.SUBMIT_ANSWER)(
            SocketHandlers.handle_submit_answer)
        SocketHandlers.SERVER.on(ClientEvent.DISCONNECT)(
            SocketHandlers.handle_disconnect)
        SocketHandlers.SERVER.on(ClientEvent.MESSAGE)(
            SocketHandlers.handle_message)

    @staticmethod
    async def handle_get_player(sid: str, _: dict) -> None:
        """Handles a player getting their player info.

        Args:
            sid (str): The socket ID of the player.
            _ (dict): The data from the client.
        """
        print(f"[backend] {sid} got player info")
        await SocketHandlers.MANAGER.get_player_info(sid)

    @staticmethod
    async def handle_new_player(sid: str, data: dict) -> None:
        """Handles a new player submitting their name.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        print(f"[backend] {sid} new player")
        event_data = NewPlayerData.from_dict(data)
        await SocketHandlers.MANAGER.new_player(sid, event_data)

    @staticmethod
    async def handle_join_lobby(sid: str, _: dict) -> None:
        """Handles a player joining the lobby.

        Args:
            sid (str): The socket ID of the player.
            _ (dict): The data from the client.
        """
        print(f"[backend] {sid} joined lobby")
        await SocketHandlers.MANAGER.join_lobby(sid)

    @staticmethod
    async def handle_join_game(sid: str, data: dict) -> None:
        """Handles a player joining a game.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        event_data = JoinGameData.from_dict(data)
        print(f"[backend] {sid} joined game {event_data.game_id}")
        await SocketHandlers.MANAGER.join_game(sid, event_data)

    @staticmethod
    async def handle_set_bot_level(sid: str, data: dict) -> None:
        """Handles a player setting the bot level.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        event_data = SetBotLevelData.from_dict(data)
        print(f"[backend] {sid} set bot level {event_data.level}")
        await SocketHandlers.MANAGER.set_bot_level(sid, event_data)

    @staticmethod
    async def handle_select_category(sid: str, data: dict) -> None:
        """Handles a player selecting a category.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        event_data = SelectCategoryData.from_dict(data)
        print(f"[backend] {sid} selected category {event_data.category}")
        await SocketHandlers.MANAGER.select_category(sid, event_data)

    @staticmethod
    async def handle_submit_answer(sid: str, data: dict) -> None:
        """Handles a player submitting an answer.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        print(f"[backend] {sid} submitted answer {data}")
        event_data = SubmitAnswerData.from_dict(data)
        SocketHandlers.MANAGER.submit_answer(sid, event_data)

    @staticmethod
    async def handle_message(_: str, data: dict) -> None:
        """Handles a player sending a message.

        Args:
            sid (str): The socket ID of the player.
            data (dict): The data from the client.
        """
        print(f"[backend] sent message {data}")
        event_data = MessageData.from_dict(data)
        await SocketHandlers.MANAGER.send_message(event_data)

    @staticmethod
    async def handle_disconnect(sid: str, _: dict) -> None:
        """Handles a player disconnecting from the server.

        Args:
            sid (str): The socket ID of the player.
            _ (dict): The data from the client.
        """
        print(f"[backend] {sid} disconnected")
        await SocketHandlers.MANAGER.disconnect(sid)
