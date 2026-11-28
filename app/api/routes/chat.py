from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from psycopg import Connection

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.message import MessageResponse
from app.services.message_service import MessageService
from app.exceptions.conversation import ConversationNotFoundError, NotConversationMemberError
from app.exceptions.user import InvalidUserTokenError
from app.services.conversation_service import ConversationService
from app.core.connection_manager import manager

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
    # Register this connection so broadcasts in this conversation reach it.
    manager.connect(conversation_id, websocket)

    message_service = MessageService(conn)                  

    try:
        while True:
            content = await websocket.receive_text()                
            # Save first. Skip blank messages.
            saved = message_service.save_message(conversation_id, user_id, content)   
            if saved is None:                                       
                continue                                            
            # Send the stored row (with id and created_at) to everyone in the room.
            await manager.broadcast(conversation_id, MessageResponse(**saved).model_dump(mode="json"))  
    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)