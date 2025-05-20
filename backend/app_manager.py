"""Manages the app."""

import socketio
from data_models import JoinGameData, LobbyUpdateData
from events import EventQueue, ServerEvent
from game_manager import GameManager
from lobby import Lobby


class AppManager:
    """Manages the app."""

    def __init__(self):
        self._lobby = Lobby()
        self._game_manager = GameManager()

        self.sio: socketio.AsyncServer | None = None

    async def run(self) -> None:
        """Runs the app manager."""
        print("[app_manager] running")
        self.sio.start_background_task(self.consume_events)

    async def consume_events(self):
        """Consumes events from the event queue."""
        print("[app_manager] consuming events")
        while True:
            event, data = await EventQueue.get()
            match event:
                case ServerEvent.LOBBY_UPDATE: await self._lobby_update(data)
                case ServerEvent.NEW_GAME: await self._new_game()

    async def add_player(self, sid: str):
        """Adds the player to the lobby."""
        print("[app_manager] add_player", sid)
        await self.sio.enter_room(sid, Lobby.ROOM)
        await self._lobby.add_player(sid)

    async def remove_player(self, sid: str):
        """Removes the player from the lobby."""
        print("[app_manager] remove_player", sid)
        await self.sio.leave_room(sid, Lobby.ROOM)
        await self._lobby.remove_player(sid)

    async def join_game(self, sid: str, data: JoinGameData):
        """Joins the player to the game.

        Args:
            data (dict): The data from the client.
        """
        print("[app_manager] join_game", sid, data)
        await self.sio.enter_room(sid, data.game_id)

    async def _lobby_update(self, data: LobbyUpdateData):
        """Emits a lobby update to the players.

        Args:
            data (LobbyUpdateData): The data to emit.
        """
        await self.sio.emit(ServerEvent.LOBBY_UPDATE, data.__dict__)
        if data.should_start_game:
            await self._new_game()

    async def _new_game(self):
        """Creates a new game and emits the game id to the players."""
        players = await self._lobby.get_players()
        await self._lobby.clear()
        # game = self._game_manager.new_game(players)
        # await self._sio.emit(ServerEvent.NEW_GAME, game.id)
