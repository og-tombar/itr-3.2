"""Manages the app."""

from data_models import JoinGameData, LobbyUpdateData
from events import EventQueue, ServerEvent
from flask import request
from flask_socketio import SocketIO, join_room, leave_room
from game_manager import GameManager
from lobby import Lobby


class AppManager:
    """Manages the app."""

    def __init__(self):
        self._sio: SocketIO | None = None
        self._lobby = Lobby()
        self._game_manager = GameManager()

    def set_sio(self, sio: SocketIO):
        """Sets the socketio instance.

        Args:
            sio (SocketIO): The socketio instance.
        """
        self._sio = sio

    def run(self) -> None:
        """Runs the app manager."""
        print("[app_manager] running")
        self._sio.start_background_task(self.consume_events)

    def consume_events(self):
        """Consumes events from the event queue."""
        while True:
            event, data = EventQueue.get()
            match event:
                case ServerEvent.LOBBY_UPDATE: self._lobby_update(data)
                case ServerEvent.NEW_GAME: self._new_game()

    def add_player(self):
        """Adds the player to the lobby."""
        print("[app_manager] add_player", request.sid)
        join_room(Lobby.ROOM)
        self._lobby.add_player(request.sid)

    def remove_player(self):
        """Removes the player from the lobby."""
        print("[app_manager] remove_player", request.sid)
        leave_room(Lobby.ROOM)
        self._lobby.remove_player(request.sid)

    def join_game(self, data: JoinGameData):
        """Joins the player to the game.

        Args:
            data (dict): The data from the client.
        """
        print("[app_manager] join_game", request.sid, data)
        join_room(data.game_id)

    def _lobby_update(self, data: LobbyUpdateData):
        """Emits a lobby update to the players.

        Args:
            data (LobbyUpdateData): The data to emit.
        """
        self._sio.emit(ServerEvent.LOBBY_UPDATE, data.__dict__)
        if data.should_start_game:
            self._new_game()

    def _new_game(self):
        """Creates a new game and emits the game id to the players."""
        print("[app_manager] new_game")
        players = self._lobby.get_players()
        self._lobby.clear()
        game = self._game_manager.new_game(players)
        self._sio.emit(ServerEvent.NEW_GAME, game.id)
