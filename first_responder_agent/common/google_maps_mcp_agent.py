"""Google Maps MCP Agent - Provides map functionality via Model Context Protocol."""

import logging
import os
from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

logger = logging.getLogger(__name__)


def on_after_maps_agent(callback_context: CallbackContext, llm_response: Optional[LlmResponse]):
    """Update map state after Google Maps agent execution."""
    try:
        # Parse the response to extract location data
        if llm_response and llm_response.content and llm_response.content.parts:
            response_text = ""
            for part in llm_response.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text

            # Try to extract location data from the response
            # The MCP tool returns structured data that we can parse
            logger.info(f"[on_after_maps_agent] Response: {response_text[:200]}...")

            # TODO: Parse the MCP response and update state
            # For now, we'll rely on the agents to manually update state

    except Exception as e:
        logger.error(f"[on_after_maps_agent] Error: {str(e)}")

    return None


def create_google_maps_mcp_agent_tool():
    """Create and return the Google Maps MCP agent wrapped as an AgentTool.

    This function creates a Google Maps agent that uses MCP (Model Context Protocol)
    and wraps it as an AgentTool so it can be called directly by other agents.
    The tool always returns control to the calling agent, even when errors occur.

    Returns:
        AgentTool: The Google Maps agent wrapped as a tool
    """
    logger.info("[create_google_maps_mcp_agent_tool] Creating Google Maps MCP agent tool")

    # Get Google Maps API key from environment
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not google_maps_api_key:
        logger.warning("[create_google_maps_mcp_agent_tool] GOOGLE_MAPS_API_KEY not set in environment")

    # Create MCP toolset for Google Maps
    mcp_toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key or ""
                }
            ),
            timeout=15,
        ),
    )

    google_maps_agent = Agent(
        name="google_maps_mcp_agent",
        model="gemini-2.5-flash",
        description="Search for nearby locations (shelters, hospitals, supplies) using Google Maps by coordinates",
        instruction="""You are a Google Maps Agent that searches for nearby locations using the Google Maps API.

CRITICAL EXECUTION RULES:
1. Use the Google Maps MCP tools to search for locations based on the provided coordinates
2. Call the appropriate MCP tool based on what is requested:
   - For nearby places: use the search/nearby tool with latitude, longitude, and place type
   - For geocoding: use the geocode tool
   - For directions: use the directions tool
3. ALWAYS return results, even if no locations are found or if an error occurs
4. Do NOT ask for clarification or additional parameters
5. Do NOT wait for user input
6. Return results in a clear, structured format

ERROR HANDLING:
- If the Google Maps API fails, return the error information in the response
- If no locations are found, return an empty result set
- ALWAYS return control to the calling agent, regardless of success or failure

RESPONSE FORMAT:
- Include location names, addresses, and coordinates
- Include distance information when available
- Keep responses concise and structured

Your task is complete once you return the search results.""",
        tools=[mcp_toolset],
        after_agent_callback=on_after_maps_agent,
    )

    # Wrap the agent as an AgentTool with skip_summarization=True
    # This ensures the raw results are passed back without additional LLM processing
    agent_tool = AgentTool(agent=google_maps_agent, skip_summarization=True)

    logger.info("[create_google_maps_mcp_agent_tool] Google Maps MCP agent tool created successfully")
    return agent_tool

