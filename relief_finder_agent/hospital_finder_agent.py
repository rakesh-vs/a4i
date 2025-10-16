"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.map_tool import find_nearby_hospitals, display_relief_resources_map

logger = logging.getLogger(__name__)


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")

    # Create sub-agent for BigQuery data access
    bq_agent = create_big_query_data_agent()

    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

Your role:
1. Use big_query_data_agent to query hospitals by location and check capacity
2. Use map tools to find nearby hospitals and display them
3. Provide hospital location, capacity, and services information
4. Help coordinate medical resources

When users ask about hospitals:
- Delegate hospital queries to big_query_data_agent
- Use find_nearby_hospitals to locate hospitals near affected areas
- Use display_relief_resources_map to visualize hospital locations""",
        tools=[find_nearby_hospitals],
        sub_agents=[bq_agent],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

