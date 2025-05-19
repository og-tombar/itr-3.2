"""Backend for the application."""

from app_manager import AppManager
from events import ClientEvent
from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
sio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
manager = AppManager()


@sio.on(ClientEvent.JOIN_LOBBY)
def handle_join_lobby(_):
    """Handles a player joining the lobby."""
    print(f"[backend] {request.sid} joined lobby")
    manager.add_player()


@sio.on(ClientEvent.JOIN_GAME)
def handle_join_game(data):
    """Handles a player joining a game.

    Args:
        data (dict): The data from the client.
    """
    print(f"[backend] {request.sid} joined game {data['game_id']}")
    manager.join_game(data)


@sio.on(ClientEvent.DISCONNECT)
def handle_disconnect():
    """Handles a player disconnecting from the server."""
    print(f"[backend] {request.sid} disconnected")
    manager.remove_player()


def run_server() -> None:
    """Runs the server."""
    manager.set_sio(sio)
    manager.run()
    sio.run(app, host='0.0.0.0', port=5000, debug=True)
