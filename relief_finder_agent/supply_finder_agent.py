"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_supply_finder_agent():
    """Create and return the Supply Finder agent."""
    logger.info("[create_supply_finder_agent] Creating Supply Finder agent")

    # Create sub-agents for BigQuery data access and map operations
    bq_agent = create_big_query_data_agent()
    maps_agent = create_google_maps_mcp_agent()

    supply_finder = Agent(
        name="supply_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available relief supplies",
        instruction="""You are the Supply Finder Sub-Agent responsible for locating relief supplies.

Your role:
1. Use big_query_data_agent to query supplies by type and location, and check inventory
2. Use google_maps_mcp_agent to find nearby supplies and display them on maps
3. Provide supply location, quantity, and contact information
4. Help coordinate supply distribution

When users ask about supplies:
- Delegate supply queries to big_query_data_agent
- Use google_maps_mcp_agent to locate supplies near affected areas
- Use google_maps_mcp_agent to visualize supply locations on maps""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

