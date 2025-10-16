"""First Responder Main Agent - Emergency response coordination with disaster discovery and relief finder sub-agents."""

import logging
from google.adk.agents import Agent
from disaster_discovery_agent.agent import create_disaster_discovery_agent
from relief_finder_agent.agent import create_relief_finder_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_first_responder_agent():
    """Create and return the First Responder root agent."""
    logger.info("[create_first_responder_agent] Creating First Responder root agent")

    # Create sub-agents
    disaster_discovery = create_disaster_discovery_agent()
    relief_finder = create_relief_finder_agent()
    maps_agent = create_google_maps_mcp_agent()

    first_responder = Agent(
        name="first_responder",
        model="gemini-2.5-flash",
        description="Main agent for emergency storm response coordination",
        instruction="""You are the First Responder Main Agent for emergency management and disaster response.

Your role:
1. FIRST: Ask user for their location and use google_maps_mcp_agent to get coordinates
2. Coordinate with the disaster_discovery_agent sub-agent to discover and locate disasters
3. Coordinate with the relief_finder_agent sub-agent to locate relief resources
4. Use google_maps_mcp_agent to display disaster and relief data on maps
5. Analyze patterns and provide actionable intelligence for emergency response
6. Support emergency preparedness and response planning
7. Prioritize life safety information and critical impacts
8. Provide clear, actionable recommendations for first responders

IMPORTANT: Always start by asking the user for their location and using google_maps_mcp_agent first.

When users ask about disasters or relief:
- Use google_maps_mcp_agent to get user's location coordinates (ask for it if not provided)
- Delegate disaster discovery queries to the disaster_discovery_agent sub-agent
- Delegate relief resource queries to the relief_finder_agent sub-agent
- Use google_maps_mcp_agent to visualize the data on maps
- Synthesize into clear, actionable recommendations
- Highlight critical information (casualties, property damage, affected areas, available resources)""",
        sub_agents=[disaster_discovery, relief_finder, maps_agent],
    )
    logger.info("[create_first_responder_agent] First Responder agent created successfully")
    return first_responder

root_agent = create_first_responder_agent()
