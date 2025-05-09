# FastAPI + LangChain Chatbot & AI Agent Template – Backend
+ [🔗 Root README](../README.md) | [🌐 Frontend README](../frontend/README.md)
+ [![Modular](https://img.shields.io/badge/Modular-Backend-blue)](#architecture--modularity)

 This is the backend component of the Next.js + FastAPI + LangChain starter template for building chatbots, RAG systems, and AI agents. It provides REST APIs for chat, file upload, document processing, and integrates with vector databases and LLMs.

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

+ ## Architecture & Modularity
+ A detailed view of backend modules and dependencies:
+ 
+ ![Backend Architecture](../docs/backend_architecture.png)
+
+ Modules:
+ - **API**: chat routes, file handlers (app/api)
+ - **Chains**: agent orchestration, prompt templates (app/chains)
+ - **Core**: config, document processing, LLM abstraction (app/core)
+ - **DB**: models, session management (app/db)
+ - **WebSocket**: streaming endpoints (app/websocket)
+
+ ## Extending the Backend
+ Learn to swap or add modules:
+ 1. **Adding a new LLM**
+    - Implement `LLMInterface` in `app/core/llm.py`.
+    - Register the new class in `config.py` and update the vectorstore initialization.
+ 2. **Integrating a different database**
+    - Create a new `DatabaseEngine` subclass in `app/db/database.py`.
+    - Adjust `models.py` and connection settings in `.env`.
+ 3. **Custom Document Processor**
+    - Extend `DocumentProcessor` in `app/core/document_processor.py`.
+    - Update workflows in `chains/agent.py`.

## License
MIT
