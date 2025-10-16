"""First Responder Main Agent - Emergency response coordination with disaster discovery and relief finder sub-agents."""

import logging
from google.adk.agents import Agent
from disaster_discovery_agent.agent import create_disaster_discovery_agent
from relief_finder_agent.agent import create_relief_finder_agent
from common.map_tool import (
    get_lat_long,
    display_disaster_map,
    display_relief_resources_map,
    display_combined_map,
)

logger = logging.getLogger(__name__)


def create_first_responder_agent():
    """Create and return the First Responder root agent."""
    logger.info("[create_first_responder_agent] Creating First Responder root agent")

    # Create sub-agents
    disaster_discovery = create_disaster_discovery_agent()
    relief_finder = create_relief_finder_agent()

    first_responder = Agent(
        name="first_responder",
        model="gemini-2.5-flash",
        description="Main agent for emergency storm response coordination",
        instruction="""You are the First Responder Main Agent for emergency management and disaster response.

Your role:
1. FIRST: Ask user for their location and call get_lat_long to get coordinates
2. Coordinate with the disaster_discovery_agent sub-agent to discover and locate disasters
3. Coordinate with the relief_finder_agent sub-agent to locate relief resources
4. Use map_tool to display disaster and relief data on maps
5. Analyze patterns and provide actionable intelligence for emergency response
6. Support emergency preparedness and response planning
7. Prioritize life safety information and critical impacts
8. Provide clear, actionable recommendations for first responders

IMPORTANT: Always start by asking the user for their location and calling get_lat_long first.

When users ask about disasters or relief:
- Call get_lat_long with user's location (ask for it if not provided)
- Delegate disaster discovery queries to the disaster_discovery_agent sub-agent
- Delegate relief resource queries to the relief_finder_agent sub-agent
- Use map_tool to visualize the data
- Synthesize into clear, actionable recommendations
- Highlight critical information (casualties, property damage, affected areas, available resources)""",
        tools=[get_lat_long, display_disaster_map, display_relief_resources_map, display_combined_map],
        sub_agents=[disaster_discovery, relief_finder],
    )
    logger.info("[create_first_responder_agent] First Responder agent created successfully")
    return first_responder

root_agent = create_first_responder_agent()
