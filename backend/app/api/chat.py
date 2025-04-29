from fastapi import APIRouter, Depends, WebSocket, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from app.db.database import get_db
from app.db.models import Chat
from app.chains.agent import create_agent
from pydantic import BaseModel

router = APIRouter()

# Store agents for different sessions
agents: Dict[str, Any] = {}

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"
    model: Optional[str] = None

class MessageResponse(BaseModel):
    content: str

@router.post("/send")
async def send_message(
    message_request: MessageRequest,
    db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    # Get or create agent for this session
    session_key = f"{message_request.session_id}_{message_request.model or 'default'}"
    
    if session_key not in agents:
        agents[session_key] = create_agent(
            message_request.session_id,
            message_request.model
        )
    
    agent = agents[session_key]
    
    # Store user message
    chat = Chat(
        session_id=message_request.session_id,
        message=message_request.message,
        is_user=True
    )
    db.add(chat)
    await db.commit()

    try:
        # Get response from agent
        response = agent.invoke({"input": message_request.message})
        ai_response = response.get("output", "I apologize, but I couldn't process that request.")

        # Store AI response
        ai_chat = Chat(
            session_id=message_request.session_id,
            message=ai_response,
            is_user=False
        )
        db.add(ai_chat)
        await db.commit()

        return MessageResponse(content=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_chat_history(
    session_id: str = "default",
    db: AsyncSession = Depends(get_db)
) -> List[dict]:
    query = select(Chat).where(Chat.session_id == session_id).order_by(Chat.timestamp)
    result = await db.execute(query)
    chats = result.scalars().all()
    
    return [
        {
            "id": chat.id,
            "message": chat.message,
            "is_user": chat.is_user,
            "timestamp": chat.timestamp
        }
        for chat in chats
    ]