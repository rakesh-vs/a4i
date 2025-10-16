"""Google Maps MCP Agent - Provides map functionality via Model Context Protocol."""

import logging
import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

logger = logging.getLogger(__name__)


def create_google_maps_mcp_agent():
    """Create and return the Google Maps MCP agent.
    
    This agent provides map functionality through the Model Context Protocol (MCP)
    using the Google Maps server.
    """
    logger.info("[create_google_maps_mcp_agent] Creating Google Maps MCP agent")
    
    # Get Google Maps API key from environment
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not google_maps_api_key:
        logger.warning("[create_google_maps_mcp_agent] GOOGLE_MAPS_API_KEY not set in environment")
    
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
        description="Sub-agent for map operations using Google Maps MCP",
        instruction="""You are the Google Maps MCP Sub-Agent responsible for all map-related operations.

Your role:
1. Find nearby locations (shelters, hospitals, supplies, etc.)
2. Display maps with various markers and overlays
3. Calculate distances and routes
4. Geocode addresses and coordinates
5. Provide location-based information

Use the Google Maps MCP tools to:
- Search for nearby places
- Display maps with custom markers
- Get location details and information
- Calculate distances between locations""",
        tools=[mcp_toolset],
    )
    logger.info("[create_google_maps_mcp_agent] Google Maps MCP agent created successfully")
    return google_maps_agent

