from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models.base import BaseChatModel
from typing import Optional
from app.core.config import settings
import google.generativeai as genai

def get_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    streaming: bool = False
) -> BaseChatModel:
    """Get an LLM instance based on the specified model."""
    callbacks = CallbackManager([StreamingStdOutCallbackHandler()]) if streaming else None
    
    model = model_name or settings.DEFAULT_MODEL
    
    # OpenAI models
    if model.startswith("gpt-"):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not set")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            api_key=settings.OPENAI_API_KEY
        )
    
    # Google Gemini models
    elif model.startswith("gemini-"):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key not set")
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            google_api_key=settings.GOOGLE_API_KEY,
            convert_system_message_to_human=True  # Required for Gemini
        )
    
    else:
        raise ValueError(f"Unknown model: {model}. Supported prefixes: 'gpt-' for OpenAI, 'gemini-' for Google")