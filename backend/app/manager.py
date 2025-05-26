"""Main application manager for coordinating services."""

import uuid

import socketio
from events.data import (GameUpdateData, JoinGameData, LobbyUpdateData,
                         MessageData, NewPlayerData, SubmitAnswerData)
from events.events import EventQueue, ServerEvent
from game.manager import GameManager
from lobby.lobby import Lobby
from player.manager import PlayerManager
from player.player import Player


class AppManager:
    """Manages the application and coordinates between services."""

    def __init__(self):
        self._lobby = Lobby()
        self._game_manager = GameManager()
        self._player_manager = PlayerManager()
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

    async def get_player_info(self, sid: str) -> None:
        """Gets a player's info.

        Args:
            sid (str): The socket id of the player.
        """
        info = self._player_manager.get_player_info(sid)
        await self.sio.emit(ServerEvent.PLAYER_INFO, info.__dict__)

    async def new_player(self, sid: str, data: NewPlayerData) -> None:
        """Creates a new player and adds them to the lobby.

        Args:
            sid (str): The socket id of the player.
            data (NewPlayerData): The data from the client.
        """
        print("[app_manager] new_player", sid, data)
        player = self._player_manager.add_player(sid, data.name)
        await self.sio.emit(ServerEvent.PLAYER_REGISTERED, sid, to=sid)
        message = MessageData(
            id=str(uuid.uuid4()),
            sender_id="0",
            username="Server",
            message=f"Hi {player.name}, and welcome to Takooh! 🐟",
        )
        await self.sio.emit(ServerEvent.MESSAGE, message.__dict__)

    async def join_lobby(self, sid: str) -> None:
        """Joins the player to the lobby.

        Args:
            sid (str): The socket id of the player.
        """
        print("[app_manager] join_lobby", sid)
        player = self._player_manager.get_player(sid)
        await self._add_to_lobby(player)

    async def join_game(self, sid: str, data: JoinGameData) -> None:
        """Joins the player to the game.

        Args:
            sid (str): The socket id of the player.
            data (JoinGameData): The data from the client.
        """
        print("[app_manager] join_game", sid, data)
        player = self._player_manager.get_player(sid)
        await self._set_room(player, data.game_id)

    def submit_answer(self, sid: str, data: SubmitAnswerData) -> None:
        """Submits an answer to the game.

        Args:
            sid (str): The socket id of the player.
            data (SubmitAnswerData): The data from the client.
        """
        print("[app_manager] submit_answer", sid, data)
        player = self._player_manager.get_player(sid)
        player.answer = data.answer

    async def send_message(self, data: MessageData) -> None:
        """Sends a message to the players.

        Args:
            sid (str): The socket id of the player.
            data (MessageData): The data to emit.
        """
        print("[app_manager] send_message", data)
        await self.sio.emit(ServerEvent.MESSAGE, data.__dict__)

    async def disconnect(self, sid: str) -> None:
        """Disconnects a player from the server.

        Args:
            sid (str): The socket id of the player.
        """
        player = self._player_manager.get_player(sid)
        await self.sio.leave_room(sid, player.room)
        self._lobby.remove_player(player)
        self._game_manager.remove_player(player)
        self._player_manager.remove_player(sid)

    ############################################################
    # Server event handlers
    ############################################################

    async def _lobby_update(self, data: LobbyUpdateData) -> None:
        """Emits a lobby update to the players.

        Args:
            data (LobbyUpdateData): The data to emit.
        """
        await self.sio.emit(ServerEvent.LOBBY_UPDATE, data.__dict__, room=Lobby.ROOM)
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
        await self.sio.emit(ServerEvent.GAME_UPDATE, game.to_dict(), room=game.id)

    ############################################################
    # Helper methods
    ############################################################

    async def _set_room(self, player: Player, room: str) -> None:
        """Sets the room for a player.

        Args:
            player (Player): The player to set the room for.
            room (str): The room to set the player in.
        """
        print("[app_manager] set_room", player, room)
        await self.sio.leave_room(player.sid, player.room)
        await self.sio.enter_room(player.sid, room)
        player.room = room

    async def _add_to_lobby(self, player: Player) -> None:
        """Adds a player to the lobby.

        Args:
            player (Player): The player to add to the lobby.
        """
        print("[app_manager] add_to_lobby", player)
        await self._set_room(player, Lobby.ROOM)
        await self._lobby.add_player(player)
