"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.big_query_data_agent import create_big_query_data_agent_tool

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

    # Create BigQuery tool
    bq_tool = create_big_query_data_agent_tool()

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- big_query_data_agent: For querying shelter data from BigQuery
- search_nearby_places: For searching shelter locations via Google Maps Places API

WORKFLOW:
1. Call the big_query_data_agent tool with the provided latitude and longitude coordinates
2. Call the search_nearby_places tool with:
   - latitude and longitude from the input
   - place_type="shelter"
   - radius=5000 (5km)
3. Synthesize shelter information from both sources
4. Format the results in natural language and return to the calling agent

EXECUTION RULES:
- Call both tools with the provided coordinates
- DO NOT stop if any tool returns an error or empty results - continue to the next step
- The search_nearby_places tool handles all map updates automatically via callbacks
- Format results as natural language summary
- Return formatted results immediately after calling both tools
- Never ask for clarification or wait for user input
""",
        tools=[bq_tool, search_nearby_places],
        before_agent_callback=on_before_shelter_agent,
        after_agent_callback=on_after_shelter_agent,
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

