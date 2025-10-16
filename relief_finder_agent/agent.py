"""Relief Finder Agent - Finds relief resources including shelters, hospitals, and supplies."""

import logging
from google.adk.agents import Agent
from relief_finder_agent.shelter_finder_agent import create_shelter_finder_agent
from relief_finder_agent.hospital_finder_agent import create_hospital_finder_agent
from relief_finder_agent.supply_finder_agent import create_supply_finder_agent

logger = logging.getLogger(__name__)


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

Your role:
1. Coordinate with shelter_finder_agent to locate shelters
2. Coordinate with hospital_finder_agent to locate medical facilities
3. Coordinate with supply_finder_agent to locate relief supplies
4. Synthesize resource information for affected areas
5. Help coordinate relief operations

When users ask about relief resources:
- Delegate shelter queries to shelter_finder_agent
- Delegate hospital queries to hospital_finder_agent
- Delegate supply queries to supply_finder_agent
- Provide comprehensive resource availability information""",
        sub_agents=[shelter_finder, hospital_finder, supply_finder],
    )
    logger.info("[create_relief_finder_agent] Relief Finder agent created successfully")
    return relief_finder

