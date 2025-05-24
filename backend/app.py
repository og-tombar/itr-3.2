"""Backend for the application."""

from contextlib import asynccontextmanager

import socketio
import uvicorn
from app_manager import AppManager
from data_models import JoinGameData, SubmitAnswerData
from events import ClientEvent
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
manager = AppManager()


@sio.on(ClientEvent.JOIN_LOBBY)
async def handle_join_lobby(sid: str, _: dict):
    """Handles a player joining the lobby."""
    print(f"[backend] {sid} joined lobby")
    await manager.add_to_lobby(sid)


@sio.on(ClientEvent.JOIN_GAME)
async def handle_join_game(sid: str, data: dict):
    """Handles a player joining a game.

    Args:
        data (dict): The data from the client.
    """
    event_data = JoinGameData.from_dict(data)
    print(f"[backend] {sid} joined game {event_data.game_id}")
    await manager.join_game(sid, event_data)


@sio.on(ClientEvent.SUBMIT_ANSWER)
async def handle_submit_answer(sid: str, data: dict):
    """Handles a player submitting an answer."""
    print(f"[backend] {sid} submitted answer {data}")
    event_data = SubmitAnswerData.from_dict(data)
    await manager.submit_answer(sid, event_data)


@sio.on(ClientEvent.DISCONNECT)
async def handle_disconnect(sid: str):
    """Handles a player disconnecting from the server."""
    print(f"[backend] {sid} disconnected")
    await manager.remove_from_lobby(sid)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize the app manager when the application starts."""
    manager.sio = sio
    await manager.run()
    yield


if __name__ == "__main__":
    app = FastAPI(lifespan=lifespan)
    sio_app = socketio.ASGIApp(sio, other_asgi_app=app)
    uvicorn.run(sio_app, host="0.0.0.0", port=8000)
