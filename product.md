## Project Title
**AI Agent Starter Template**  
*(Stack: Next.js + FastAPI + LangChain + SQLite)*

---

## 1. Objective
Create a **developer-friendly**, **production-ready** starter template for building **chat-focused AI agents**, **RAG systems**, and **LLM apps**, using:
- **Next.js frontend** (interactive UI)
- **FastAPI backend** (APIs, WebSockets, file uploads)
- **LangChain pipelines** (agents, chains, RAG)
- **SQLite** (chat history and file metadata storage)

Designed for rapid development, scaling, and extension.

---

## 2. Target Users
- AI/ML Engineers
- Fullstack Developers
- Hackathon Teams
- AI Product Startups
- Research Tools Builders

---

## 3. Functional Requirements

### Frontend (Next.js)
- Chat Interface
- Show past conversations
- Upload files globally (not tied to a chat)
- Real-time streaming responses
- Dark/Light mode theming

### Backend (FastAPI)
- REST APIs
  - `/chat/send` — Send user message and get response
  - `/chat/history` — Retrieve chat history
  - `/files/upload` — Upload a document (pdf, txt, csv)
  - `/files/list` — List uploaded files
- WebSocket for real-time message streaming
- Store:
  - **Chats** in **SQLite**
  - **File Metadata** in **SQLite**
  - **Uploaded Files** in local `uploads/` directory
- LangChain Integration:
  - Default RAG pipeline using uploaded files
  - Default agent chain

### Database (SQLite)
- **Tables**
  - `chats` — id, session_id, message, is_user, timestamp
  - `files` — id, filename, filepath, upload_time

---

## 4. Non-Functional Requirements
- Responsive UI (mobile/desktop)
- Performance: Response under 2s for standard prompts
- Basic file size limit (e.g., 10MB/file)
- Security:
  - Validate uploaded files
  - API keys handled securely
- Scalability consideration: easy migration to PostgreSQL later
- Code Quality: 
  - Type hints
  - Linters (ESLint, Prettier, Ruff, Black)

---

## 5. Tech Stack

| Layer            | Technology                 |
| ---------------- | --------------------------- |
| Frontend         | Next.js 14 (App Router), TailwindCSS |
| Backend          | FastAPI, LangChain           |
| LLM Integrations | OpenAI API / HuggingFace models |
| Database         | SQLite                       |
| Vectorstore      | Chroma / FAISS (modular)      |
| Storage          | Local filesystem (`/uploads`) |
| Deployment       | Docker + Vercel/Render ready |

---

## 6. File Structure

```
/ai-agent-starter/
├── frontend/ (Next.js 14 App Router)
│   ├── app/
│   │   ├── page.tsx (Main Chat Page)
│   │   ├── upload/ (File upload UI)
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── InputBox.tsx
│   │   ├── FileUpload.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   └── useUpload.ts
│   ├── utils/
│   │   └── api.ts (axios setup)
│   ├── public/
│   └── tailwind.config.ts
│
├── backend/ (FastAPI + LangChain)
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── file.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── llm.py
│   │   │   ├── vectorstore.py
│   │   ├── chains/
│   │   │   ├── rag_chain.py
│   │   │   └── agent_chain.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── crud.py
│   │   ├── websocket/
│   │   │   └── connection.py
│   │   └── main.py (FastAPI app instance)
│   ├── uploads/ (uploaded files stored here)
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 7. API Overview

| Method  | Endpoint           | Description                   |
| ------- | ------------------ | ----------------------------- |
| POST    | `/chat/send`        | Send a message and receive reply |
| GET     | `/chat/history`     | Fetch previous chat history |
| POST    | `/files/upload`     | Upload a document file |
| GET     | `/files/list`       | List uploaded files |

---

## 8. Setup Instructions

**Quick Start:**
```bash
# 1. Clone the repo
git clone https://github.com/your-org/ai-agent-starter.git
cd ai-agent-starter

# 2. Setup backend
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Setup frontend
cd ../frontend
pnpm install
pnpm dev

# 4. Access
Frontend: http://localhost:3000
Backend: http://localhost:8000
```

**Environment Variables:**

- `/backend/.env`
```env
OPENAI_API_KEY=your-openai-api-key
VECTORSTORE_DIR=./data/vectorstore
UPLOAD_DIR=./uploads
DATABASE_URL=sqlite:///./app.db
```

- `/frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---
