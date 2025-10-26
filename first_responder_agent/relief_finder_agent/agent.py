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

CRITICAL: You will receive coordinates (latitude, longitude) from the first_responder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS - REGARDLESS OF RESULTS:

AUTOMATIC EXECUTION SEQUENCE (DO NOT SKIP ANY STEP - EVEN IF RESULTS ARE EMPTY):
1. IMMEDIATELY delegate to shelter_finder_agent to locate shelters using the provided coordinates
   - CONTINUE REGARDLESS OF WHETHER SHELTERS ARE FOUND OR NOT
2. IMMEDIATELY delegate to hospital_finder_agent to locate medical facilities using the provided coordinates
   - CONTINUE REGARDLESS OF WHETHER HOSPITALS ARE FOUND OR NOT
3. IMMEDIATELY delegate to supply_finder_agent to locate relief supplies using the provided coordinates
   - CONTINUE REGARDLESS OF WHETHER SUPPLIES ARE FOUND OR NOT
4. Synthesize all resource information for affected areas
5. Return complete relief resource information to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- DO NOT stop after any single agent call - CONTINUE EVEN IF RESULTS ARE EMPTY
- Execute all three agent calls in sequence WITHOUT EXCEPTION
- Collect results from ALL THREE agents before synthesizing (even if some are empty)
- Synthesize all resource data into a comprehensive report
- Include all available resources and capacity information
- Provide complete resource availability information
- Return results immediately without waiting for user input
- IMPORTANT: Empty results from one agent do NOT mean you should stop - continue to the next agent

Your role:
1. Coordinate with shelter_finder_agent to locate shelters
2. Coordinate with hospital_finder_agent to locate medical facilities
3. Coordinate with supply_finder_agent to locate relief supplies
4. Synthesize resource information for affected areas
5. Help coordinate relief operations

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        sub_agents=[shelter_finder, hospital_finder, supply_finder],
        before_agent_callback=on_before_relief_agent,
        after_agent_callback=on_after_relief_agent,
    )
    logger.info("[create_relief_finder_agent] Relief Finder agent created successfully")
    return relief_finder

