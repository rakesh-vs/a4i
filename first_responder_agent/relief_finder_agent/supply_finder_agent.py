"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import check_supply_inventory

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

    supply_finder = Agent(
        name="supply_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available relief supplies",
        instruction="""You are the Supply Finder Sub-Agent responsible for locating relief supplies.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- check_supply_inventory: For querying supply data from BigQuery (currently placeholder)
- search_nearby_places: For searching supply locations via Google Maps Places API

WORKFLOW - EXECUTE ALL STEPS:
1. Call the search_nearby_places tool with:
   - latitude and longitude from the input
   - place_type="pharmacy" (pharmacies often have emergency supplies)
   - radius=5000 (5km)
   ⚠️ CRITICAL: After receiving the result, IMMEDIATELY proceed to Step 2. DO NOT STOP.
2. The search_nearby_places tool automatically updates the map with supply locations
3. Synthesize supply information from the search results
4. Format the results in natural language and return to the calling agent

EXECUTION RULES:
- Execute all steps in sequence without stopping between steps
- DO NOT STOP after receiving any tool result - continue to the next step
- DO NOT wait for user input between steps
- If any step returns an error or no data, acknowledge it and continue to the next step
- The search_nearby_places tool handles all map updates automatically via callbacks
- Format results as natural language summary
- Never ask for clarification
""",
        tools=[check_supply_inventory, search_nearby_places],
        before_agent_callback=on_before_supply_agent,
        after_agent_callback=on_after_supply_agent,
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder
