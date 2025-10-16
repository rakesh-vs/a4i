"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")

    # Create sub-agents for BigQuery data access and map operations
    bq_agent = create_big_query_data_agent()
    maps_agent = create_google_maps_mcp_agent()

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

Your role:
1. Use big_query_data_agent to query shelters by location and check capacity
2. Use google_maps_mcp_agent to find nearby shelters and display them on maps
3. Provide shelter location, capacity, and contact information
4. Help coordinate shelter resources

When users ask about shelters:
- Delegate shelter queries to big_query_data_agent
- Use google_maps_mcp_agent to locate shelters near affected areas
- Use google_maps_mcp_agent to visualize shelter locations on maps""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

