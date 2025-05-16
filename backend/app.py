"""Backend for the application."""

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


@socketio.on('ping_event')
def handle_ping(data):
    """Handle ping event.

    Args:
        data (_type_): A pong message.
    """
    print(f"[backend] got ping: {data}")
    emit('pong_event', {'message': 'pong'}, room=request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
