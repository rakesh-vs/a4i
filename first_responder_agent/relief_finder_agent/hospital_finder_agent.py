"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import check_hospital_capacity

logger = logging.getLogger(__name__)


def on_before_hospital_agent(callback_context: CallbackContext):
    """Update agent activity when hospital finder starts."""
    update_agent_activity(callback_context.state, "hospital_finder_agent", "running")
    logger.info("[on_before_hospital_agent] Hospital finder agent started")
    return None


def on_after_hospital_agent(callback_context: CallbackContext):
    """Update agent activity when hospital finder completes."""
    update_agent_activity(callback_context.state, "hospital_finder_agent", "completed")
    logger.info("[on_after_hospital_agent] Hospital finder agent completed")
    return None


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")

    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- check_hospital_capacity: For querying hospital data from BigQuery (currently placeholder)
- search_nearby_places: For searching hospital locations via Google Maps Places API

WORKFLOW - EXECUTE ALL STEPS:
1. Call the search_nearby_places tool with:
   - latitude and longitude from the input
   - place_type="hospital"
   - radius=5000 (5km)
   ⚠️ CRITICAL: After receiving the result, IMMEDIATELY proceed to Step 2. DO NOT STOP.
2. The search_nearby_places tool automatically updates the map with hospital locations
3. Synthesize hospital information from the search results
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
        tools=[check_hospital_capacity, search_nearby_places],
        before_agent_callback=on_before_hospital_agent,
        after_agent_callback=on_after_hospital_agent,
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder
