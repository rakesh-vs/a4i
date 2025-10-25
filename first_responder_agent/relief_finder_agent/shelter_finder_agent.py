"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent
from ..common.big_query_data_agent import create_big_query_data_agent_tool
from ..common.google_maps_mcp_agent import create_google_maps_mcp_agent_tool

logger = logging.getLogger(__name__)


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")

    # Create BigQuery and Google Maps tools
    bq_tool = create_big_query_data_agent_tool()
    maps_tool = create_google_maps_mcp_agent_tool()

    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

You will receive coordinates (latitude, longitude) from the relief_finder_agent.

You have access to TWO TOOLS:
- big_query_data_agent TOOL: For querying shelter data from BigQuery
- google_maps_mcp_agent TOOL: For searching shelter locations via Google Maps

WORKFLOW:
1. Call the big_query_data_agent TOOL with the provided latitude and longitude coordinates
2. Call the google_maps_mcp_agent TOOL with the provided coordinates and specify place type (e.g., "shelter", "emergency_shelter")
3. Synthesize shelter information from both sources into a comprehensive report
4. Return complete shelter data to the calling agent using the transfer_to_agent tool

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
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

