"""
LangChain React-style prebuilt agent for query processing and response generation.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from src.settings import settings
from foundry.observability import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)

def process_query(query: str) -> str:
    """
    Process a user query using the React agent and return a response.
    
    Args:
        query (str): The user's query/question
        
    Returns:
        str: The agent's response
    """
    with tracer.start_as_current_span("process_query"):
        try:
            logger.info(f"Processing query: {query}")
            
            # Get the agent executor
            llm = ChatOpenAI(
                    model="gpt-5.4-nano",
                    api_key=settings.openai_api_key,
                    temperature=0.3,
                )
            
            system_prompt = f"You are a helpful assistant. Answer the following question: {query}"
            agent = create_agent(llm, tools=None, system_prompt=system_prompt)
            
            # Run the agent with the query
            result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            response = result["messages"][-1].content if result.get("messages") else "I'm sorry, I couldn't generate a response."
            
            logger.info(f"Generated response: {response}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return f"Error processing query: {str(e)}"
