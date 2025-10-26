"""Disaster Discovery Agent - Discovers and locates disasters using BigQuery, FEMA Live, and NOAA Live data."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..common.big_query_data_agent import create_big_query_data_agent_tool
from ..common.state_tools import update_agent_activity
from .fema_live_agent.agent import create_fema_live_agent
from .noaa_live_agent.agent import create_noaa_live_agent

logger = logging.getLogger(__name__)


def on_before_disaster_agent(callback_context: CallbackContext):
    """Update agent activity when disaster discovery starts."""
    update_agent_activity(callback_context.state, "disaster_discovery_agent", "running")
    logger.info("[on_before_disaster_agent] Disaster discovery agent started")
    return None


def on_after_disaster_agent(callback_context: CallbackContext):
    """Update agent activity when disaster discovery completes."""
    update_agent_activity(callback_context.state, "disaster_discovery_agent", "completed")
    logger.info("[on_after_disaster_agent] Disaster discovery agent completed")
    return None


def create_disaster_discovery_agent():
    """Create and return the Disaster Discovery agent."""
    logger.info("[create_disaster_discovery_agent] Creating Disaster Discovery agent")

    # Create BigQuery tool and sub-agents
    bq_tool = create_big_query_data_agent_tool()
    fema_live_agent = create_fema_live_agent()
    noaa_live_agent = create_noaa_live_agent()

    disaster_discovery = Agent(
        name="disaster_discovery_agent",
        model="gemini-2.5-pro",
        description="Sub-agent for discovering and locating disasters",
        instruction="""You are the Disaster Discovery Sub-Agent responsible for finding and locating disasters.

You will receive coordinates (latitude, longitude) from the first_responder_agent.

WORKFLOW - EXECUTE ALL 5 STEPS SEQUENTIALLY, NO EXCEPTIONS:
Step 1:
Use the big_query_data_agent TOOL with the coordinates to query ongoing storm data.
⚠️ CRITICAL: If this returns NO results or an error, IGNORE IT and IMMEDIATELY proceed to Step 2.

Step 2:
Handoff to fema_live_agent sub-agent with the coordinates to query FEMA disaster data.
⚠️ CRITICAL: If this returns NO results or an error, IGNORE IT and IMMEDIATELY proceed to Step 3.

Step 3:
Handoff to noaa_live_agent sub-agent with the coordinates to query NOAA weather alerts.
⚠️ CRITICAL: If this returns NO results or an error, IGNORE IT and IMMEDIATELY proceed to Step 4.

Step 4:
Synthesize ALL disaster data collected from Steps 1-3 into a comprehensive report.
Even if some steps returned no data, create a report with what you have.

Step 5:
Return the synthesized disaster information and transfer control back to the calling agent using the transfer_to_agent tool.

EXECUTION RULES:
- Do all 5 steps regardless of their result, do not stop at any point.
- ⚠️ CRITICAL: DO NOT STOP IF ANY TOOL RETURNS AN ERROR - CONTINUE TO THE NEXT STEP.
- Never ask for clarification and never wait for user input.

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.
Never stop to ask for clarification or additional input.
""",
        tools=[bq_tool],
        sub_agents=[fema_live_agent, noaa_live_agent],
        before_agent_callback=on_before_disaster_agent,
        after_agent_callback=on_after_disaster_agent,
    )
    logger.info("[create_disaster_discovery_agent] Disaster Discovery agent created successfully")
    return disaster_discovery

