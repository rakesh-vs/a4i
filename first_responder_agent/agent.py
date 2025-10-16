"""First Responder Main Agent - Emergency response coordination with disaster discovery, relief finder, and insights sub-agents."""

import logging
from google.adk.agents import Agent
from .disaster_discovery_agent.agent import create_disaster_discovery_agent
from .relief_finder_agent.agent import create_relief_finder_agent
from .insights_agent.agent import create_insights_agent
from .common.geocoding import geocode_location

logger = logging.getLogger(__name__)


def create_first_responder_agent():
    """Create and return the First Responder root agent."""
    logger.info("[create_first_responder_agent] Creating First Responder root agent")

    # Create sub-agents
    disaster_discovery = create_disaster_discovery_agent()
    relief_finder = create_relief_finder_agent()
    insights = create_insights_agent()

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
5. IMMEDIATELY call insights_agent with ALL collected disaster and relief data to synthesize final analysis
6. Return the final comprehensive analysis from insights_agent to the user

EXECUTION RULES:
- Ask for location ONLY if not provided by user
- After getting location, DO NOT ask for any more user confirmation
- DO NOT wait for user input between steps 2-6
- Execute each step immediately after the previous one completes
- Pass all collected data to the next agent in the chain
- Ensure insights_agent receives complete disaster AND relief data for synthesis
- This is a continuous automated workflow after location is obtained
- Use the geocode_location tool to convert location strings to coordinates

Your role:
- Coordinate with disaster_discovery_agent to discover and locate disasters
- Coordinate with relief_finder_agent to locate relief resources
- Delegate to insights_agent to synthesize data into comprehensive analysis and action plans
- Provide clear, actionable recommendations for first responders

IMPORTANT: Once location is obtained, execute all remaining steps in sequence without user intervention.""",
        tools=[geocode_location],
        sub_agents=[disaster_discovery, relief_finder, insights],
    )
    logger.info("[create_first_responder_agent] First Responder agent created successfully")
    return first_responder

root_agent = create_first_responder_agent()
