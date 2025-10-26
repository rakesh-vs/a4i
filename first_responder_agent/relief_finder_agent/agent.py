"""Relief Finder Agent - Finds relief resources including shelters, hospitals, and supplies."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.state_tools import update_agent_activity
from .shelter_finder_tool import find_shelters
from .hospital_finder_tool import find_hospitals
from .supply_finder_tool import find_supplies

logger = logging.getLogger(__name__)


def on_before_relief_agent(callback_context: CallbackContext):
    """Update agent activity when relief finder starts."""
    update_agent_activity(callback_context.state, "relief_finder_agent", "running")
    logger.info("[on_before_relief_agent] Relief finder agent started")
    return None


def on_after_relief_agent(callback_context: CallbackContext):
    """Update agent activity when relief finder completes."""
    update_agent_activity(callback_context.state, "relief_finder_agent", "completed")
    logger.info("[on_after_relief_agent] Relief finder agent completed")
    return None


def create_relief_finder_agent():
    """Create and return the Relief Finder agent."""
    logger.info("[create_relief_finder_agent] Creating Relief Finder agent")

    relief_finder = Agent(
        name="relief_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding relief resources",
        instruction="""You are the Relief Finder Sub-Agent responsible for locating relief resources.

You will receive coordinates (latitude, longitude) from the first_responder_agent.

🚨 MANDATORY WORKFLOW - YOU MUST CALL ALL 3 TOOLS IN SEQUENCE 🚨

You have access to THREE TOOLS:
- find_shelters: Finds emergency shelters and lodging facilities
- find_hospitals: Finds hospitals and medical facilities
- find_supplies: Finds pharmacies and supply locations

STEP 1: SHELTERS (REQUIRED)
Call the find_shelters tool with the provided latitude and longitude coordinates.
Wait for result, then IMMEDIATELY go to Step 2. DO NOT STOP.

STEP 2: HOSPITALS (REQUIRED)
Call the find_hospitals tool with the provided latitude and longitude coordinates.
Wait for result, then IMMEDIATELY go to Step 3. DO NOT STOP.

STEP 3: SUPPLIES (REQUIRED)
Call the find_supplies tool with the provided latitude and longitude coordinates.
Wait for result, then IMMEDIATELY go to Step 4. DO NOT STOP.

STEP 4: SYNTHESIZE (REQUIRED)
Create a comprehensive summary of ALL THREE resource types (shelters, hospitals, supplies).
Include results even if some tools found nothing.
Format the results in natural language.
Then IMMEDIATELY go to Step 5. DO NOT STOP.

STEP 5: RETURN (REQUIRED)
Call transfer_to_agent to return to the calling agent.

⚠️ CRITICAL RULES ⚠️
- YOU MUST COMPLETE ALL 5 STEPS - NO EXCEPTIONS
- DO NOT STOP after Step 1 (shelters) - you MUST continue to hospitals and supplies
- DO NOT STOP after Step 2 (hospitals) - you MUST continue to supplies
- DO NOT STOP after Step 3 (supplies) - you MUST synthesize and return
- Empty results from any tool DO NOT mean you should stop
- NEVER ask for user input or clarification
- NEVER stop before completing all 5 steps
- All tools automatically update the map with their findings

If you stop before Step 5, you have FAILED your task.
""",
        tools=[find_shelters, find_hospitals, find_supplies],
        before_agent_callback=on_before_relief_agent,
        after_agent_callback=on_after_relief_agent,
    )
    logger.info("[create_relief_finder_agent] Relief Finder agent created successfully")
    return relief_finder

