"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.map_tool import find_nearby_supplies, display_relief_resources_map

logger = logging.getLogger(__name__)


def create_supply_finder_agent():
    """Create and return the Supply Finder agent."""
    logger.info("[create_supply_finder_agent] Creating Supply Finder agent")

    # Create sub-agent for BigQuery data access
    bq_agent = create_big_query_data_agent()

    supply_finder = Agent(
        name="supply_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available relief supplies",
        instruction="""You are the Supply Finder Sub-Agent responsible for locating relief supplies.

Your role:
1. Use big_query_data_agent to query supplies by type and location, and check inventory
2. Use map tools to find nearby supplies and display them
3. Provide supply location, quantity, and contact information
4. Help coordinate supply distribution

When users ask about supplies:
- Delegate supply queries to big_query_data_agent
- Use find_nearby_supplies to locate supplies near affected areas
- Use display_relief_resources_map to visualize supply locations""",
        tools=[find_nearby_supplies],
        sub_agents=[bq_agent],
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

