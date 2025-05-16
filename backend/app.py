"""Backend for the application."""

from dataclasses import dataclass

from flask import Flask, request
from flask_socketio import SocketIO, join_room
from matchmaking import Lobby


@dataclass
class AppState:
    """The state of the application."""
    lobby: Lobby = Lobby()


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
state = AppState()


@socketio.on('join_lobby')
def handle_join_lobby(_):
    """
    Handle a player joining the lobby.
    This function is called when a player joins the lobby.
    It adds the player to the lobby and emits the lobby update to all players in the lobby.
    """
    sid = request.sid
    print(f"[backend] join_lobby from {sid}")
    state.lobby.add_player(sid)
    update = state.lobby.get_update()
    join_room(Lobby.ROOM)
    socketio.emit('lobby_update', update, room=Lobby.ROOM)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
