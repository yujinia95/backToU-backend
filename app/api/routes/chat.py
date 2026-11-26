from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["chat"])


@router.websocket("/conversations/{conversation_id}")
async def chat_endpoint(websocket: WebSocket, conversation_id: int):
    # Accept the handshake. Nothing can be sent or received before this.
    await websocket.accept()

    try:
        while True:
            # Wait until this client sends a message.
            message = await websocket.receive_text()
            # Send the same text back to the same client.
            await websocket.send_text(f"echo: {message}")
    except WebSocketDisconnect:
        print(f"Client left conversation {conversation_id}")
