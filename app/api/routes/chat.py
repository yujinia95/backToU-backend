from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from psycopg import Connection

from app.core.database import get_db
from app.core.security import verify_token
from app.exceptions.conversation import ConversationNotFoundError, NotConversationMemberError
from app.exceptions.user import InvalidUserTokenError
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/ws", tags=["chat"])


@router.websocket("/conversations/{conversation_id}")
async def chat_endpoint(
    websocket: WebSocket,
    conversation_id: int,
    conn: Annotated[Connection, Depends(get_db)],
    token: str | None = None,
):
    # Reject the handshake when no token was sent.
    if token is None:
        await websocket.close(code=1008)
        return

    # Reject the handshake when the token is invalid or expired.
    try:
        user_id = verify_token(token)
    except InvalidUserTokenError:
        await websocket.close(code=1008)
        return    

    # Reject the handshake when the user is not in this conversation.
    try:
        ConversationService(conn).check_membership(conversation_id, user_id)
    except (ConversationNotFoundError, NotConversationMemberError):
        await websocket.close(code=1008)
        return


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
