from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
import os
from typing import List
from app.core.vectorstore import get_vectorstore

def process_document(file_path: str) -> None:
    """Process a document and add it to the vector store."""
    # Determine file type and use appropriate loader
    if file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type for {file_path}")
    
    # Load the document
    documents = loader.load()
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Add to vector store
    vectorstore = get_vectorstore()
    vectorstore.add_documents(splits)
    vectorstore.persist()