from typing import List, Optional
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, LLMResult
from app.core.vectorstore import get_vectorstore
from app.core.config import settings
import asyncio

class StreamingHandler(BaseCallbackHandler):
    """Callback handler for streaming responses."""
    
    def __init__(self):
        self.tokens = []
        self.streaming_callback = None

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run when a new token is generated."""
        if self.streaming_callback:
            self.streaming_callback(token)
        self.tokens.append(token)

    def set_streaming_callback(self, callback):
        """Set the callback for streaming tokens."""
        self.streaming_callback = callback

def create_agent(session_id: str, model: Optional[str] = None, streaming_callback=None):
    """Create an agent with the given session ID and model."""
    
    # Initialize streaming handler
    streaming_handler = StreamingHandler()
    if streaming_callback:
        streaming_handler.set_streaming_callback(streaming_callback)
    
    # Initialize LLM with streaming
    llm = ChatOpenAI(
        model=model or settings.DEFAULT_MODEL,
        temperature=0.7,
        streaming=True,
        callbacks=[streaming_handler]
    )
    
    # Initialize memory with error handling
    try:
        history = ChatMessageHistory()
        memory = ConversationBufferMemory(
            chat_memory=history,
            memory_key="chat_history",
            return_messages=True
        )
    except Exception as e:
        print(f"Error initializing memory: {e}")
        # Fallback to basic memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    # Initialize vector store with retry logic
    max_retries = 3
    retry_delay = 1
    vectorstore = None
    
    for attempt in range(max_retries):
        try:
            vectorstore = get_vectorstore()
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to initialize vectorstore after {max_retries} attempts: {e}")
                raise
            print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
            asyncio.sleep(retry_delay)
            retry_delay *= 2

    # Create retrieval tool with error handling
    retrieval_tool = Tool(
        name="search_documents",
        description="Search through uploaded documents for relevant information. Use this tool to find specific facts or context from the documents.",
        func=lambda q: _safe_retrieval(vectorstore, q)
    )

    tools = [retrieval_tool]

    # Create prompt with improved system message
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant with access to document search capabilities.
        Your primary task is to help users understand and work with their documents.
        
        Guidelines:
        1. Always use the search_documents tool first when asked about specific information
        2. Be concise but thorough in your responses
        3. If you're unsure about something, acknowledge it and explain what you do know
        4. When citing information from documents, briefly mention the source
        5. Format your responses for readability when appropriate
        
        Remember: Your goal is to be helpful while maintaining accuracy and clarity."""),
        MessagesPlaceholder(variable_name="chat_history"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create agent with error handling
    try:
        agent = create_openai_functions_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )
    except Exception as e:
        print(f"Error creating agent: {e}")
        # Fallback to simpler prompt if needed
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant."),
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_functions_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )

def _safe_retrieval(vectorstore, query: str) -> str:
    """Safely perform retrieval with error handling."""
    try:
        docs = vectorstore.as_retriever().get_relevant_documents(query)
        return "\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"Error during document retrieval: {e}")
        return "I apologize, but I couldn't access the document storage at the moment. Please try again."