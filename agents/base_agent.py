"""Base agent configuration and utilities."""

from typing import Optional, List
from google.adk.agents import Agent
from google.adk.tools import google_search


class BaseAgentConfig:
    """Configuration for creating agents."""
    
    DEFAULT_MODEL = "gemini-2.5-flash"
    DEFAULT_TEMPERATURE = 0.7
    
    @staticmethod
    def create_agent(
        name: str,
        instruction: str,
        description: str,
        model: Optional[str] = None,
        tools: Optional[List] = None,
    ) -> Agent:
        """
        Create an agent with the given configuration.
        
        Args:
            name: Agent name
            instruction: System instruction for the agent
            description: Agent description
            model: LLM model to use (defaults to gemini-2.5-flash)
            tools: List of tools available to the agent
            
        Returns:
            Configured Agent instance
        """
        if model is None:
            model = BaseAgentConfig.DEFAULT_MODEL
        
        if tools is None:
            tools = [google_search]
        
        return Agent(
            name=name,
            model=model,
            instruction=instruction,
            description=description,
            tools=tools,
        )

