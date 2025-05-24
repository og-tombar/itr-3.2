"""Main entry point for the backend application."""

from contextlib import asynccontextmanager

import socketio
import uvicorn
from api.socket import SocketHandlers
from app.manager import AppManager
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
manager = AppManager()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize the app manager when the application starts.

    Args:
        _ (FastAPI): The FastAPI application.
    """
    manager.sio = sio
    SocketHandlers.setup(sio, manager)
    await manager.run()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: The FastAPI application.
    """
    app = FastAPI(
        title="Trivia Game Backend",
        description="Backend API for the trivia game application",
        version="1.0.0",
        lifespan=lifespan
    )
    return app


def main():
    """Main entry point for the backend application."""
    app = create_app()
    sio_app = socketio.ASGIApp(sio, other_asgi_app=app)
    uvicorn.run(sio_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
