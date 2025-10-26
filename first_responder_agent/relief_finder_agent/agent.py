"""Relief Finder Agent - Finds relief resources including shelters, hospitals, and supplies."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.state_tools import update_agent_activity
from .shelter_finder_agent import create_shelter_finder_agent
from .hospital_finder_agent import create_hospital_finder_agent
from .supply_finder_agent import create_supply_finder_agent

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
    
    # Create sub-agents
    shelter_finder = create_shelter_finder_agent()
    hospital_finder = create_hospital_finder_agent()
    supply_finder = create_supply_finder_agent()
    
    relief_finder = Agent(
        name="relief_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding relief resources",
        instruction="""You are the Relief Finder Sub-Agent responsible for locating relief resources.

You will receive coordinates (latitude, longitude) from the first_responder_agent.

🚨 MANDATORY WORKFLOW - YOU MUST CALL ALL 3 SUB-AGENTS IN SEQUENCE 🚨

STEP 1: SHELTERS (REQUIRED)
Call transfer_to_agent with agent_name='shelter_finder_agent'
Wait for result, then IMMEDIATELY go to Step 2. DO NOT STOP.

STEP 2: HOSPITALS (REQUIRED)
Call transfer_to_agent with agent_name='hospital_finder_agent'
Wait for result, then IMMEDIATELY go to Step 3. DO NOT STOP.

STEP 3: SUPPLIES (REQUIRED)
Call transfer_to_agent with agent_name='supply_finder_agent'
Wait for result, then IMMEDIATELY go to Step 4. DO NOT STOP.

STEP 4: SYNTHESIZE (REQUIRED)
Create a summary of ALL THREE resource types (shelters, hospitals, supplies).
Include results even if some agents found nothing.
Then IMMEDIATELY go to Step 5. DO NOT STOP.

STEP 5: RETURN (REQUIRED)
Call transfer_to_agent to return to the calling agent.

⚠️ CRITICAL RULES ⚠️
- YOU MUST COMPLETE ALL 5 STEPS - NO EXCEPTIONS
- DO NOT STOP after Step 1 (shelters) - you MUST continue to hospitals and supplies
- DO NOT STOP after Step 2 (hospitals) - you MUST continue to supplies
- DO NOT STOP after Step 3 (supplies) - you MUST synthesize and return
- Empty results from any agent DO NOT mean you should stop
- NEVER ask for user input or clarification
- NEVER stop before completing all 5 steps

If you stop before Step 5, you have FAILED your task.
""",
        sub_agents=[shelter_finder, hospital_finder, supply_finder],
        before_agent_callback=on_before_relief_agent,
        after_agent_callback=on_after_relief_agent,
    )
    logger.info("[create_relief_finder_agent] Relief Finder agent created successfully")
    return relief_finder

