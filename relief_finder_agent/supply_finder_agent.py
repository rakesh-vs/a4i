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

CRITICAL: You will receive coordinates (latitude, longitude) from the relief_finder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS:

AUTOMATIC EXECUTION:
1. IMMEDIATELY use big_query_data_agent to query supplies at the provided coordinates
2. Check supply inventory and availability
3. Synthesize supply information into a comprehensive report
4. Return complete supply data to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- Execute queries automatically with the provided coordinates
- Return all available supply information
- Include location, quantity, and contact information
- Return results immediately without waiting for user input

Your role:
1. Use big_query_data_agent to query supplies by type and location, and check inventory
2. Provide supply location, quantity, and contact information
3. Help coordinate supply distribution""",
        sub_agents=[bq_agent],
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

