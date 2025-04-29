import typer
import uvicorn
import asyncio
from typing import Optional
from app.chains.agent import create_agent
from app.db.database import AsyncSessionLocal
from app.db.models import Chat

app = typer.Typer()

async def save_interaction(session_id: str, message: str, is_user: bool):
    async with AsyncSessionLocal() as db:
        chat = Chat(
            session_id=session_id,
            message=message,
            is_user=is_user
        )
        db.add(chat)
        await db.commit()

@app.command()
def chat(
    session_id: Optional[str] = typer.Option("cli", "--session-id", "-s", help="Session ID for the chat"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Model to use (e.g., 'anthropic/claude-2', 'openai/gpt-4', 'google/gemini-pro')"),
    message: Optional[str] = typer.Argument(None, help="Message to send to the AI")
):
    """Start an interactive chat session with the AI or send a single message."""
    agent = create_agent(session_id, model)
    
    async def process_message(msg: str):
        # Save user message
        await save_interaction(session_id, msg, True)
        
        # Get AI response
        response = agent.invoke({"input": msg})
        ai_response = response.get("output", "I apologize, but I couldn't process that request.")
        
        # Save AI response
        await save_interaction(session_id, ai_response, False)
        
        return ai_response

    model_info = f" using {model}" if model else ""
    if message:
        # Single message mode
        response = asyncio.run(process_message(message))
        typer.echo(f"\nAI{model_info}: {response}\n")
    else:
        # Interactive mode
        typer.echo(f"Starting interactive chat session{model_info} (type 'exit' to quit)")
        typer.echo("----------------------------------------")
        
        while True:
            # Get user input
            user_input = typer.prompt("\nYou")
            
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Process message and show response
            response = asyncio.run(process_message(user_input))
            typer.echo(f"\nAI{model_info}: {response}")

@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
    reload: bool = typer.Option(True, "--reload/--no-reload")
):
    """Start the FastAPI server"""
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    app()