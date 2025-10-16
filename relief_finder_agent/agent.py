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

CRITICAL: You will receive coordinates (latitude, longitude) from the first_responder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS:

AUTOMATIC EXECUTION SEQUENCE:
1. IMMEDIATELY delegate to shelter_finder_agent to locate shelters using the provided coordinates
2. IMMEDIATELY delegate to hospital_finder_agent to locate medical facilities using the provided coordinates
3. IMMEDIATELY delegate to supply_finder_agent to locate relief supplies using the provided coordinates
4. Synthesize all resource information for affected areas
5. Return complete relief resource information to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- Execute all queries automatically with the provided coordinates
- Synthesize all resource data into a comprehensive report
- Include all available resources and capacity information
- Provide complete resource availability information
- Return results immediately without waiting for user input

Your role:
1. Coordinate with shelter_finder_agent to locate shelters
2. Coordinate with hospital_finder_agent to locate medical facilities
3. Coordinate with supply_finder_agent to locate relief supplies
4. Synthesize resource information for affected areas
5. Help coordinate relief operations""",
        sub_agents=[shelter_finder, hospital_finder, supply_finder],
    )
    logger.info("[create_relief_finder_agent] Relief Finder agent created successfully")
    return relief_finder

