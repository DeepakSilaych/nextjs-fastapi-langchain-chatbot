import typer
import uvicorn
from app.cli import app as cli_app

app = typer.Typer()
app.add_typer(cli_app, name="chat")

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