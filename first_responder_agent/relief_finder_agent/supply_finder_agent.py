"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.big_query_data_agent import create_big_query_data_agent_tool

logger = logging.getLogger(__name__)


def on_before_supply_agent(callback_context: CallbackContext):
    """Update agent activity when supply finder starts."""
    update_agent_activity(callback_context.state, "supply_finder_agent", "running")
    logger.info("[on_before_supply_agent] Supply finder agent started")
    return None


def on_after_supply_agent(callback_context: CallbackContext):
    """Update agent activity when supply finder completes."""
    update_agent_activity(callback_context.state, "supply_finder_agent", "completed")
    logger.info("[on_after_supply_agent] Supply finder agent completed")
    return None


def create_supply_finder_agent():
    """Create and return the Supply Finder agent."""
    logger.info("[create_supply_finder_agent] Creating Supply Finder agent")

    # Create BigQuery tool
    bq_tool = create_big_query_data_agent_tool()

    supply_finder = Agent(
        name="supply_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available relief supplies",
        instruction="""You are the Supply Finder Sub-Agent responsible for locating relief supplies.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- big_query_data_agent: For querying supply data from BigQuery
- search_nearby_places: For searching supply locations via Google Maps Places API

WORKFLOW:
1. Call the big_query_data_agent tool with the provided latitude and longitude coordinates
2. Call the search_nearby_places tool with:
   - latitude and longitude from the input
   - place_type="pharmacy" (pharmacies often have emergency supplies)
   - radius=5000 (5km)
3. The search_nearby_places tool automatically updates the map with supply locations
4. Synthesize supply information from both sources
5. Format the results in natural language and return to the calling agent

EXECUTION RULES:
- Call both tools with the provided coordinates
- DO NOT stop if any tool returns an error or empty results - continue to the next step
- The search_nearby_places tool handles all map updates automatically via callbacks
- Format results as natural language summary
- Return formatted results immediately after calling both tools
- Never ask for clarification or wait for user input
""",
        tools=[bq_tool, search_nearby_places],
        before_agent_callback=on_before_supply_agent,
        after_agent_callback=on_after_supply_agent,
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

