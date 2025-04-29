# Backend – AI Chat Application

This is the backend service for the AI Chat Application, built with FastAPI. It provides REST APIs for chat, file upload, document processing, and integrates with vector databases and LLMs.

## Features
- FastAPI-based REST API
- File upload and document processing (PDF, TXT)
- Vector database integration (ChromaDB)
- Chat session and message management (SQLite)
- LangChain and OpenAI integration
- WebSocket support for real-time features

## Requirements
- Python 3.12+
- (Recommended) [Poetry](https://python-poetry.org/) or `venv` for virtual environments
- Docker (optional, for containerized deployment)

## Setup (Local Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   - Create a `.env` file or export variables in your shell:
     ```
     OPENAI_API_KEY=your-openai-api-key
     # Optionally override upload/data directories
     # UPLOAD_DIR=uploads
     # VECTORSTORE_DIR=data/vectorstore
     ```

5. **Run the server**
   ```bash
   python manage.py serve
   # or with uvicorn directly:
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Docker Usage

1. **Build and run with Docker**
   ```bash
   docker build -t ai-chat-backend .
   docker run -d -p 8000:8000 --env OPENAI_API_KEY=your-openai-api-key ai-chat-backend
   ```
   Or use the root `docker-compose.yml` for multi-service orchestration.

2. **Volumes**
   - Uploaded files: `uploads/`
   - Vectorstore data: `data/vectorstore/`

## API Endpoints

### Chat
- `POST /chat/send` — Send a message and get a response
- `GET /chat/history` — Retrieve chat history
- `GET /chat/sessions` — List chat sessions
- `GET /chat/stream` — Stream chat responses (WebSocket)

### Files
- `POST /files/upload` — Upload a document (PDF, TXT)
- `GET /files/list` — List uploaded files

## Project Structure
```
backend/
  app/
    api/         # API route handlers
    chains/      # LLM chains and logic
    core/        # Core config, document processing, vectorstore
    db/          # Database models and session
    websocket/   # WebSocket handlers
    main.py      # FastAPI app entrypoint
  data/          # Vectorstore data
  uploads/       # Uploaded files
  requirements.txt
  Dockerfile
  manage.py      # CLI for running the app
```

## Environment Variables
- `OPENAI_API_KEY` (required): Your OpenAI API key
- `UPLOAD_DIR` (optional): Directory for uploaded files (default: `uploads/`)
- `VECTORSTORE_DIR` (optional): Directory for vectorstore data (default: `data/vectorstore/`)

## Development Notes
- All uploaded files and vectorstore data are persisted in mounted volumes (see Dockerfile and docker-compose).
- The backend is CORS-enabled for local frontend development.
- For production, review CORS and security settings.

## License
MIT
