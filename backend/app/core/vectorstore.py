from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
import os

def get_vectorstore():
    embeddings = OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY
    )
    
    # Create vectorstore directory if it doesn't exist
    os.makedirs(settings.VECTORSTORE_DIR, exist_ok=True)
    
    return Chroma(
        persist_directory=settings.VECTORSTORE_DIR,
        embedding_function=embeddings
    )