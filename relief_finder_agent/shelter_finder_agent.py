"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.map_tool import find_nearby_shelters, display_relief_resources_map

logger = logging.getLogger(__name__)


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")

    # Create sub-agent for BigQuery data access
    bq_agent = create_big_query_data_agent()

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

Your role:
1. Use big_query_data_agent to query shelters by location and check capacity
2. Use map tools to find nearby shelters and display them
3. Provide shelter location, capacity, and contact information
4. Help coordinate shelter resources

When users ask about shelters:
- Delegate shelter queries to big_query_data_agent
- Use find_nearby_shelters to locate shelters near affected areas
- Use display_relief_resources_map to visualize shelter locations""",
        tools=[find_nearby_shelters],
        sub_agents=[bq_agent],
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

