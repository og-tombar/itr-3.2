"""Backend for the application."""

from dataclasses import dataclass

from flask import Flask, request
from flask_socketio import SocketIO, join_room
from matchmaking import Lobby


@dataclass
class Context:
    """The Context class holds the state of the application."""
    lobby: Lobby = Lobby()


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
context = Context()


@socketio.on('join_lobby')
def handle_join_lobby(_):
    """
    Handle a player joining the lobby.
    This function is called when a player joins the lobby.
    It adds the player to the lobby and emits the lobby update to all players in the lobby.
    """
    sid = request.sid
    print(f"[backend] join_lobby from {sid}")
    join_room(Lobby.ROOM)
    context.lobby.add_player(sid)
    lobby_state = context.lobby.get_state()
    socketio.emit('lobby_update', lobby_state.players)

    if lobby_state.should_game_start:
        print("[backend] starting game")
        game_state = context.lobby.start_game()
        for p in game_state.players:
            join_room(game_state.id, sid=p)
        socketio.emit('game_start', game_state.__dict__, room=game_state.id)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
