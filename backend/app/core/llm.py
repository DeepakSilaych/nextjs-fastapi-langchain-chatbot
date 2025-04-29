from langchain_openai import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Optional
from app.core.config import settings

class OpenRouterLLM(ChatOpenAI):
    """OpenRouter LLM implementation"""
    
    def __init__(
        self,
        model_name: str = "openai/gpt-3.5-turbo",
        temperature: float = 0.7,
        streaming: bool = False,
        callbacks: Optional[CallbackManager] = None,
    ):
        super().__init__(
            model=model_name,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            openai_api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            http_headers={
                "HTTP-Referer": "http://localhost:3000",  # Required for OpenRouter
                "X-Title": "AI Chat App",  # Optional, shown in OpenRouter dashboard
            }
        )

def get_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    streaming: bool = False
) -> BaseChatModel:
    """
    Get an LLM instance based on the model name.
    Supports both OpenAI and OpenRouter models.
    """
    callbacks = CallbackManager([StreamingStdOutCallbackHandler()]) if streaming else None
    
    model = model_name or settings.DEFAULT_MODEL
    
    if model.startswith("openai/"):
        # Use OpenRouter for OpenAI models
        return OpenRouterLLM(
            model_name=model,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks
        )
    elif model.startswith("anthropic/") or model.startswith("google/") or model.startswith("meta/"):
        # Use OpenRouter for other providers
        return OpenRouterLLM(
            model_name=model,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks
        )
    else:
        # Default to standard OpenAI
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            api_key=settings.OPENAI_API_KEY
        )