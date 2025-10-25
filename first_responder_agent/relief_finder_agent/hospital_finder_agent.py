"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent
from ..common.big_query_data_agent import create_big_query_data_agent_tool
from ..common.google_maps_mcp_agent import create_google_maps_mcp_agent_tool

logger = logging.getLogger(__name__)


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")

    # Create BigQuery and Google Maps tools
    bq_tool = create_big_query_data_agent_tool()
    maps_tool = create_google_maps_mcp_agent_tool()

    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- big_query_data_agent TOOL: For querying hospital data from BigQuery
- google_maps_mcp_agent TOOL: For searching hospital locations via Google Maps

WORKFLOW:
1. Use the big_query_data_agent TOOL with the latitude and longitude coordinates
2. Use the google_maps_mcp_agent TOOL with the latitude and longitude coordinates and specify place type (e.g., "hospital", "medical_facility")
3. Synthesize hospital information from both sources into a comprehensive report
4. Return complete data to the calling agent using the transfer_to_agent tool.

EXECUTION RULES:
- Do all 4 steps regardless of their result, do not stop at any point.
- ⚠️ CRITICAL: DO NOT STOP IF ANY TOOL RETURNS AN ERROR - CONTINUE TO THE NEXT STEP.
- Never ask for clarification and never wait for user input.

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.
Never stop to ask for clarification or additional input.
""",
        tools=[bq_tool, maps_tool],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

