"""
LangChain React-style prebuilt agent for query processing and response generation.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.callbacks import get_usage_metadata_callback

from src.settings import settings
from foundry.observability import get_logger, get_tracer
from foundry.llm_utils import get_usage_cost, UsageCost, Model

logger = get_logger(__name__)
tracer = get_tracer(__name__)

def process_query(query: str) -> tuple[str, UsageCost | None]:
    """
    Process a user query using the React agent and return a response.
    
    Args:
        query (str): The user's query/question
        
    Returns:
        tuple[str, UsageCost | None]: The agent's response and usage cost
    """
    with tracer.start_as_current_span("process_query"):
        try:
            logger.info(f"Processing query: {query}")
            
            # Get the agent executor
            llm = ChatOpenAI(
                    model=Model.GPT_54_NANO,
                    api_key=settings.openai_api_key,
                    temperature=0.3,
                )
            
            system_prompt = f"You are a helpful assistant. Answer the following question: {query}"
            agent = create_agent(llm, tools=None, system_prompt=system_prompt)
            
            # Run the agent with the query, capturing usage metadata (input/output tokens)
            with get_usage_metadata_callback() as usage_cb:
                result = agent.invoke({"messages": [{"role": "user", "content": query}]})
            
            # get usage cost
            usage_cost: UsageCost = get_usage_cost(usage_cb)
            
            response = result["messages"][-1].content if result.get("messages") else "I'm sorry, I couldn't generate a response."
            
            logger.info(f"Generated response: {response}")
            
            return response, usage_cost
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return f"Error processing query: {str(e)}", None