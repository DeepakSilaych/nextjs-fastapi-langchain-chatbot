import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.database import get_db
from app.db.models import File as FileModel
from app.core.config import settings
from app.core.document_processor import process_document
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class FileResponse(BaseModel):
    id: int
    filename: str
    upload_time: datetime

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> FileResponse:
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Validate file type
    if not file.filename.endswith(('.txt', '.pdf')):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are supported"
        )
    
    # Save file to uploads directory
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
            
        # Process the document and add to vector store
        process_document(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Save file info to database
    db_file = FileModel(
        filename=file.filename,
        filepath=file_path
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    
    return FileResponse(
        id=db_file.id,
        filename=db_file.filename,
        upload_time=db_file.upload_time
    )

@router.get("/list")
async def list_files(
    db: AsyncSession = Depends(get_db)
) -> List[FileResponse]:
    query = select(FileModel).order_by(FileModel.upload_time.desc())
    result = await db.execute(query)
    files = result.scalars().all()
    
    return [
        FileResponse(
            id=file.id,
            filename=file.filename,
            upload_time=file.upload_time
        )
        for file in files
    ]