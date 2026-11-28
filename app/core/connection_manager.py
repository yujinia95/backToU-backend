from fastapi import WebSocket


class ConnectionManager:
    """Keeps the open WebSockets of each conversation in memory."""

    def __init__(self) -> None:
        # conversation_id -> list of open WebSockets in that conversation
        self.active: dict[int, list[WebSocket]] = {}

    def connect(self, conversation_id: int, websocket: WebSocket) -> None:
        # add websocket to this conversation's list
        if conversation_id not in self.active:
            self.active[conversation_id] = []

        self.active[conversation_id].append(websocket)

    def disconnect(self, conversation_id: int, websocket: WebSocket) -> None:
        # remove websocket from this conversation's list
        self.active[conversation_id].remove(websocket)
        # If everyone has left and the list is empty,
        # remove this conversation's key.
        if not self.active[conversation_id]:
            del self.active[conversation_id]

    async def broadcast(self, conversation_id: int, message: dict) -> None:
        # send message to every websocket in this conversation
        for websocket in self.active.get(conversation_id, []):
            await websocket.send_json(message)
        
# One shared manager for the whole app.
manager = ConnectionManager()