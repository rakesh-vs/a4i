"""First Responder Main Agent - Emergency response coordination with disaster discovery, relief finder, and insights tool."""

import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .disaster_discovery_agent.agent import create_disaster_discovery_agent
from .relief_finder_agent.agent import create_relief_finder_agent
from .insights_agent.agent import create_insights_tool
from .common.geocoding import geocode_location
from .common.state_tools import update_agent_activity

logger = logging.getLogger(__name__)


def on_before_agent(callback_context: CallbackContext):
    """Initialize state before agent execution."""
    if "locations" not in callback_context.state:
        callback_context.state["locations"] = []

    if "center" not in callback_context.state:
        callback_context.state["center"] = {"lat": 37.7749, "lng": -122.4194}

    if "currentAgent" not in callback_context.state:
        callback_context.state["currentAgent"] = None

    if "activityHistory" not in callback_context.state:
        callback_context.state["activityHistory"] = []

    # Update current agent activity
    agent_name = callback_context.agent_name
    if agent_name:
        update_agent_activity(callback_context.state, agent_name, "running")
        logger.info(f"[on_before_agent] Agent started: {agent_name}")

    return None


def on_after_agent(callback_context: CallbackContext):
    """Update state after agent execution."""
    agent_name = callback_context.agent_name
    if agent_name:
        update_agent_activity(callback_context.state, agent_name, "completed")
        logger.info(f"[on_after_agent] Agent completed: {agent_name}")

    return None


def create_first_responder_agent():
    """Create and return the First Responder root agent."""
    logger.info("[create_first_responder_agent] Creating First Responder root agent")

    # Create sub-agents
    disaster_discovery = create_disaster_discovery_agent()
    relief_finder = create_relief_finder_agent()

    # Create insights tool (wraps agent to hide output from UI)
    insights_tool = create_insights_tool()

    first_responder = Agent(
        name="first_responder",
        model="gemini-2.5-flash",
        description="Main agent for emergency storm response coordination",
        instruction="""You are the First Responder Main Agent for emergency management and disaster response.

CRITICAL: Execute the following workflow AUTOMATICALLY WITHOUT STOPPING BETWEEN STEPS:

WORKFLOW EXECUTION SEQUENCE:
1. IF user location is not provided: Ask user for their location ONCE, then immediately proceed to step 2
2. Convert the location string to latitude/longitude coordinates using the geocode_location tool
3. IMMEDIATELY call disaster_discovery_agent with the coordinates to discover disasters
4. IMMEDIATELY call relief_finder_agent with the coordinates to locate relief resources
5. IMMEDIATELY call insights_agent tool with ALL collected disaster and relief data to synthesize final analysis
6. Present the final comprehensive analysis from insights_agent to the user

EXECUTION RULES:
- Ask for location ONLY if not provided by user
- After getting location, DO NOT ask for any more user confirmation
- DO NOT wait for user input between steps 2-6
- Execute each step immediately after the previous one completes
- Pass all collected data to the next step in the chain
- Ensure insights_agent tool receives complete disaster AND relief data for synthesis
- This is a continuous automated workflow after location is obtained
- Use the geocode_location tool to convert location strings to coordinates
- Use the insights_agent tool to synthesize the final analysis

Your role:
- Coordinate with disaster_discovery_agent to discover and locate disasters
- Coordinate with relief_finder_agent to locate relief resources
- Use insights_agent tool to synthesize data into comprehensive analysis and action plans
- Present the final analysis to the user.

IMPORTANT: Once location is obtained, execute all remaining steps in sequence without user intervention.""",
        tools=[geocode_location, insights_tool],
        sub_agents=[disaster_discovery, relief_finder],
        before_agent_callback=on_before_agent,
        after_agent_callback=on_after_agent,
    )
    logger.info("[create_first_responder_agent] First Responder agent created successfully")
    return first_responder

root_agent = create_first_responder_agent()
