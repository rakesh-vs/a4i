"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent
from ..common.big_query_data_agent import create_big_query_data_agent
from ..common.google_maps_mcp_agent import create_google_maps_mcp_agent

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

IMPORTANT: You have TWO sub-agents available:
- big_query_data_agent: For querying supply data from BigQuery
- google_maps_mcp_agent: For searching supply distribution center locations via Google Maps

AUTOMATIC EXECUTION:
1. IMMEDIATELY delegate to big_query_data_agent with the provided coordinates
   - Pass the coordinates to big_query_data_agent
   - It will check supply inventory and availability
2. IMMEDIATELY delegate to google_maps_mcp_agent with the provided coordinates
   - Pass the coordinates to google_maps_mcp_agent
   - It will search for supply distribution center locations
   - IF Google Maps fails, CONTINUE ANYWAY with BigQuery results
3. Synthesize supply information into a comprehensive report
4. Return complete supply data to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- DO NOT try to call any functions directly - only delegate to sub-agents
- Execute queries automatically with the provided coordinates
- Return all available supply information
- Include location, quantity, and contact information
- Return results immediately without waiting for user input
- IF BigQuery data retrieval fails, CONTINUE with Google Maps results - DO NOT STOP
- Partial results are acceptable - return what you have

Your role:
1. Delegate to big_query_data_agent to check supply inventory and availability
2. Delegate to google_maps_mcp_agent to search for supply distribution center locations
3. Provide supply location, quantity, and contact information
4. Help coordinate supply distribution

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

