from fastapi import APIRouter, Depends, WebSocket, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict, Any, Optional, AsyncGenerator
import json
import asyncio
from app.db.database import get_db
from app.db.models import Chat
from app.chains.agent import create_agent
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Store agents for different sessions
agents: Dict[str, Any] = {}

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"
    model: Optional[str] = None

class MessageResponse(BaseModel):
    content: str

class ChatSession(BaseModel):
    id: str
    title: str
    timestamp: datetime
    message_count: int

async def save_chat(db: AsyncSession, session_id: str, message: str, is_user: bool):
    """Helper function to save chat messages to the database."""
    chat = Chat(
        session_id=session_id,
        message=message,
        is_user=is_user
    )
    db.add(chat)
    await db.commit()

async def generate_response(agent: Any, message: str, db: AsyncSession, session_id: str) -> AsyncGenerator[str, None]:
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: agent.invoke({"input": message})
        )
        ai_response = response.get("output", "I apologize, but I couldn't process that request.")
        
        # Store the complete AI response in the database
        await save_chat(db, session_id, ai_response, False)
        
        # Split response into chunks and stream
        chunks = [ai_response[i:i+5] for i in range(0, len(ai_response), 5)]
        for chunk in chunks:
            yield f"data: {json.dumps({'content': chunk})}\n\n"
            await asyncio.sleep(0.05)  # Add small delay between chunks
            
        yield "event: done\ndata: {}\n\n"
        
    except Exception as e:
        error_message = str(e)
        # Store error response in database
        await save_chat(db, session_id, f"Error: {error_message}", False)
        yield f"data: {json.dumps({'error': error_message})}\n\n"
        yield "event: done\ndata: {}\n\n"

@router.get("/stream")
async def stream_chat(
    message: str,
    session_id: str = "default",
    model: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> StreamingResponse:
    # Get or create agent for this session
    session_key = f"{session_id}_{model or 'default'}"
    
    if session_key not in agents:
        agents[session_key] = create_agent(session_id, model)
    
    agent = agents[session_key]
    
    # Store user message
    await save_chat(db, session_id, message, True)

    return StreamingResponse(
        generate_response(agent, message, db, session_id),
        media_type="text/event-stream"
    )

@router.get("/sessions")
async def get_chat_sessions(db: AsyncSession = Depends(get_db)) -> List[ChatSession]:
    # Get unique session IDs with their latest message and message count
    query = select(
        Chat.session_id,
        func.max(Chat.timestamp).label("latest_timestamp"),
        func.count().label("message_count"),
        func.substring(func.min(Chat.message), 1, 50).label("first_message")  # Use first 50 chars of first message as title
    ).group_by(Chat.session_id)
    
    result = await db.execute(query)
    sessions = result.all()
    
    return [
        ChatSession(
            id=session.session_id,
            title=session.first_message + "..." if len(session.first_message or "") > 47 else session.first_message,
            timestamp=session.latest_timestamp,
            message_count=session.message_count
        )
        for session in sessions
    ]

# Keep existing /send endpoint for non-streaming requests
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
    await save_chat(db, message_request.session_id, message_request.message, True)

    try:
        # Get response from agent
        response = agent.invoke({"input": message_request.message})
        ai_response = response.get("output", "I apologize, but I couldn't process that request.")

        # Store AI response
        await save_chat(db, message_request.session_id, ai_response, False)

        return MessageResponse(content=ai_response)
    except Exception as e:
        error_message = str(e)
        # Store error response
        await save_chat(db, message_request.session_id, f"Error: {error_message}", False)
        raise HTTPException(status_code=500, detail=error_message)

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