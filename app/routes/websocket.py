from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.services.websocket_manager import (
    manager,
)

print("WEBSOCKET ROUTER LOADED")
router = APIRouter()


@router.websocket("/ws/fleet")
async def fleet_socket(
    websocket: WebSocket,
):

    await manager.connect(websocket)

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)
