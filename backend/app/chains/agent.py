from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from app.core.vectorstore import get_vectorstore
from app.core.llm import get_llm
from typing import Optional

def create_agent(session_id: str = "default", model: Optional[str] = None):
    # Initialize the language model
    llm = get_llm(
        model_name=model,
        temperature=0.7
    )
    
    # Initialize vector store and create retrieval tool
    vectorstore = get_vectorstore()
    
    # Create retrieval tool
    retrieval_tool = Tool(
        name="search_documents",
        description="Search through uploaded documents for relevant information.",
        func=vectorstore.as_retriever().get_relevant_documents
    )
    
    # Define tools
    tools = [retrieval_tool]
    
    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        agent_kwargs={
            "system_message": SystemMessage(
                content="""You are a helpful AI assistant with access to document search capabilities.
                Use the search_documents tool when asked about specific information that might be in uploaded documents.
                Always be polite and professional in your responses."""
            ),
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
        }
    )
    
    return agent