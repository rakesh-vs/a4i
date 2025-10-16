"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")

    # Create sub-agents for BigQuery data access and map operations
    bq_agent = create_big_query_data_agent()
    maps_agent = create_google_maps_mcp_agent()

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

CRITICAL: You will receive coordinates (latitude, longitude) from the relief_finder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS:

AUTOMATIC EXECUTION:
1. IMMEDIATELY use google_maps_mcp_agent to search for nearby shelters at the provided coordinates
2. Use big_query_data_agent to query shelters at the provided coordinates for additional data
   - IF BigQuery fails, CONTINUE ANYWAY with Google Maps results
3. Check shelter capacity and availability
4. Synthesize shelter information into a comprehensive report
5. Return complete shelter data to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- Execute queries automatically with the provided coordinates
- Return all available shelter information
- Include location, capacity, and contact information
- Return results immediately without waiting for user input
- IF BigQuery data retrieval fails, CONTINUE with Google Maps results - DO NOT STOP
- Partial results are acceptable - return what you have

Your role:
1. Use google_maps_mcp_agent to find nearby shelters using the provided coordinates
2. Use big_query_data_agent to query shelters by location and check capacity
3. Provide shelter location, capacity, and contact information
4. Help coordinate shelter resources

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

