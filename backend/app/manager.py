"""Main application manager for coordinating services."""

import socketio
from events.data import (GameUpdateData, JoinGameData, LobbyUpdateData,
                         MessageData, SubmitAnswerData)
from events.events import EventQueue, ServerEvent
from game.manager import GameManager
from lobby.lobby import Lobby


class AppManager:
    """Manages the application and coordinates between services."""

    def __init__(self):
        self._lobby = Lobby()
        self._game_manager = GameManager()
        self.sio: socketio.AsyncServer | None = None

    async def run(self) -> None:
        """Runs the app manager."""
        self.sio.start_background_task(self.consume_events)

    async def consume_events(self) -> None:
        """Consumes server events from the event queue."""
        while True:
            event, data = await EventQueue.get()
            match event:
                case ServerEvent.LOBBY_UPDATE: await self._lobby_update(data)
                case ServerEvent.NEW_GAME: await self._new_game()
                case ServerEvent.GAME_UPDATE: await self._game_update(data)

    ############################################################
    # Client event handlers
    ############################################################

    async def add_to_lobby(self, sid: str) -> None:
        """Adds the player to the lobby.

        Args:
            sid (str): The socket id of the player.
        """
        print("[app_manager] add_to_lobby", sid)
        await self.sio.enter_room(sid, Lobby.ROOM)
        await self._lobby.add_player(sid)

    async def remove_from_lobby(self, sid: str) -> None:
        """Removes the player from the lobby.

        Args:
            sid (str): The socket id of the player.
        """
        print("[app_manager] remove_from_lobby", sid)
        await self.sio.leave_room(sid, Lobby.ROOM)
        self._lobby.remove_player(sid)

    async def join_game(self, sid: str, data: JoinGameData) -> None:
        """Joins the player to the game.

        Args:
            sid (str): The socket id of the player.
            data (JoinGameData): The data from the client.
        """
        print("[app_manager] join_game", sid, data)
        await self.sio.leave_room(sid, Lobby.ROOM)
        await self.sio.enter_room(sid, data.game_id)

    async def submit_answer(self, sid: str, data: SubmitAnswerData) -> None:
        """Submits an answer to the game.

        Args:
            sid (str): The socket id of the player.
            data (SubmitAnswerData): The data from the client.
        """
        print("[app_manager] submit_answer", sid, data)
        await self._game_manager.submit_answer(sid, data)

    async def send_message(self, data: MessageData) -> None:
        """Sends a message to the players.

        Args:
            sid (str): The socket id of the player.
            data (MessageData): The data to emit.
        """
        print("[app_manager] send_message", data)
        await self.sio.emit(ServerEvent.MESSAGE, data.__dict__)

    ############################################################
    # Server event handlers
    ############################################################

    async def _lobby_update(self, data: LobbyUpdateData) -> None:
        """Emits a lobby update to the players.

        Args:
            data (LobbyUpdateData): The data to emit.
        """
        await self.sio.emit(ServerEvent.LOBBY_UPDATE, data.__dict__)
        if data.should_start_game:
            await self._new_game()

    async def _new_game(self) -> None:
        """Created a new game and emits the game id to the players."""
        players = self._lobby.get_players()
        game = self._game_manager.new_game(players)
        await self.sio.emit(ServerEvent.NEW_GAME, game.__dict__, room=Lobby.ROOM)
        self._lobby.clear()

    async def _game_update(self, game: GameUpdateData) -> None:
        """Emits the game update to the players.

        Args:
            game (GameUpdateData): The game data to emit.
        """
        print("[app_manager] game_update", game)
        await self.sio.emit(ServerEvent.GAME_UPDATE, game.__dict__, room=game.id)
