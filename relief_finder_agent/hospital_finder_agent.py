"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")

    # Create sub-agents for BigQuery data access and map operations
    bq_agent = create_big_query_data_agent()
    maps_agent = create_google_maps_mcp_agent()

    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

Your role:
1. Use big_query_data_agent to query hospitals by location and check capacity
2. Use google_maps_mcp_agent to find nearby hospitals and display them on maps
3. Provide hospital location, capacity, and services information
4. Help coordinate medical resources

When users ask about hospitals:
- Delegate hospital queries to big_query_data_agent
- Use google_maps_mcp_agent to locate hospitals near affected areas
- Use google_maps_mcp_agent to visualize hospital locations on maps""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

