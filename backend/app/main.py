from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, files
from app.db.database import engine
from app.db.models import Base

app = FastAPI(title="AI Chat API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(files.router, prefix="/files", tags=["files"])

# Create database tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)