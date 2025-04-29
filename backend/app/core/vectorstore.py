from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from app.core.config import settings
import os

def get_vectorstore():
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
    
    # Create vectorstore directory if it doesn't exist
    os.makedirs(settings.VECTORSTORE_DIR, exist_ok=True)
    
    client = chromadb.PersistentClient(path=settings.VECTORSTORE_DIR)
    
    return Chroma(
        embedding_function=embeddings,
        client=client,
        collection_name="documents"
    )