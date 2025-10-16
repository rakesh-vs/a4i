"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from common.google_maps_mcp_agent import create_google_maps_mcp_agent

logger = logging.getLogger(__name__)


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")

    # Create sub-agents for BigQuery data access and map operations
    bq_agent = create_big_query_data_agent()
    maps_agent = create_google_maps_mcp_agent()

    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

CRITICAL: You will receive coordinates (latitude, longitude) from the relief_finder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS:

IMPORTANT: You have TWO sub-agents available:
- big_query_data_agent: For querying hospital data from BigQuery
- google_maps_mcp_agent: For searching hospital locations via Google Maps

AUTOMATIC EXECUTION:
1. IMMEDIATELY delegate to big_query_data_agent with the provided coordinates
   - Pass the coordinates to big_query_data_agent
   - It will check hospital capacity and services
2. IMMEDIATELY delegate to google_maps_mcp_agent with the provided coordinates
   - Pass the coordinates to google_maps_mcp_agent
   - It will search for hospital locations
   - IF Google Maps fails, CONTINUE ANYWAY with BigQuery results
3. Synthesize hospital information into a comprehensive report
4. Return complete hospital data to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- DO NOT try to call any functions directly - only delegate to sub-agents
- Execute queries automatically with the provided coordinates
- Return all available hospital information
- Include location, capacity, and services information
- Return results immediately without waiting for user input
- IF BigQuery data retrieval fails, CONTINUE with Google Maps results - DO NOT STOP
- Partial results are acceptable - return what you have

Your role:
1. Delegate to big_query_data_agent to check hospital capacity and services
2. Delegate to google_maps_mcp_agent to search for hospital locations
3. Provide hospital location, capacity, and services information
4. Help coordinate medical resources

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        sub_agents=[bq_agent, maps_agent],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

