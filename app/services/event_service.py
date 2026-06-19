import asyncio

from app.services.websocket_manager import (
    manager,
)


def publish_event(payload: dict):

    try:

        loop = asyncio.get_running_loop()

        loop.create_task(manager.broadcast(payload))

    except RuntimeError:

        asyncio.run(manager.broadcast(payload))
