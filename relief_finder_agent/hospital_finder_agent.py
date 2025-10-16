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

AUTOMATIC EXECUTION:
1. IMMEDIATELY use big_query_data_agent to query hospitals at the provided coordinates
2. Check hospital capacity and services
3. Synthesize hospital information into a comprehensive report
4. Return complete hospital data to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- Execute queries automatically with the provided coordinates
- Return all available hospital information
- Include location, capacity, and services information
- Return results immediately without waiting for user input

Your role:
1. Use big_query_data_agent to query hospitals by location and check capacity
2. Provide hospital location, capacity, and services information
3. Help coordinate medical resources""",
        sub_agents=[bq_agent],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

