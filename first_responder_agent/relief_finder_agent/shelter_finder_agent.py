"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import get_available_shelter_info

logger = logging.getLogger(__name__)


def on_before_shelter_agent(callback_context: CallbackContext):
    """Update agent activity when shelter finder starts."""
    update_agent_activity(callback_context.state, "shelter_finder_agent", "running")
    logger.info("[on_before_shelter_agent] Shelter finder agent started")
    return None


def on_after_shelter_agent(callback_context: CallbackContext):
    """Update agent activity when shelter finder completes."""
    update_agent_activity(callback_context.state, "shelter_finder_agent", "completed")
    logger.info("[on_after_shelter_agent] Shelter finder agent completed")
    return None


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- get_available_shelter_info: For querying shelter data from BigQuery
- search_nearby_places: For searching shelter locations via Google Maps Places API

WORKFLOW - EXECUTE ALL STEPS:
1. Call the get_available_shelter_info tool with the provided latitude and longitude coordinates
   ⚠️ CRITICAL: After receiving the result, IMMEDIATELY proceed to Step 2. DO NOT STOP.
2. Call the search_nearby_places tool with:
   - latitude and longitude from the input
   - place_type="shelter"
   - radius=5000 (5km)
   ⚠️ CRITICAL: After receiving the result, IMMEDIATELY proceed to Step 3. DO NOT STOP.
3. Synthesize shelter information from both sources
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
        tools=[get_available_shelter_info, search_nearby_places],
        before_agent_callback=on_before_shelter_agent,
        after_agent_callback=on_after_shelter_agent,
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

