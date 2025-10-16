"""Search agent implementation."""

from google.adk.agents import Agent
from google.adk.tools import google_search
from agents.base_agent import BaseAgentConfig


def create_search_agent() -> Agent:
    """
    Create a search assistant agent.
    
    Returns:
        Agent configured for web search
    """
    return BaseAgentConfig.create_agent(
        name="search_assistant",
        instruction="""You are a helpful search assistant. 
        Your job is to help users find information by searching the web when needed.
        Always provide accurate, relevant, and well-organized information.
        If you don't know something, use the search tool to find the answer.
        Format your responses clearly with sections and bullet points when appropriate.""",
        description="An assistant that can search the web to answer questions",
        tools=[google_search],
    )

