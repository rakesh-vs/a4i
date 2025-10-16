"""Disaster Discovery Agent - Discovers and locates disasters using BigQuery and FEMA data."""

import logging
from google.adk.agents import Agent
from disaster_discovery_agent.bq_agent.agent import create_bigquery_agent
from disaster_discovery_agent.fema_agent.agent import create_fema_agent
from disaster_discovery_agent.location_finder import find_disaster_location, geocode_address

logger = logging.getLogger(__name__)


def create_disaster_discovery_agent():
    """Create and return the Disaster Discovery agent."""
    logger.info("[create_disaster_discovery_agent] Creating Disaster Discovery agent")
    
    # Create sub-agents
    bq_agent = create_bigquery_agent()
    fema_agent = create_fema_agent()
    
    disaster_discovery = Agent(
        name="disaster_discovery_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for discovering and locating disasters",
        instruction="""You are the Disaster Discovery Sub-Agent responsible for finding and locating disasters.

Your role:
1. Query historical storm data from the bigquery_agent sub-agent
2. Query live FEMA disaster data from the fema_agent sub-agent
3. Use location_finder tools to determine geographic locations
4. Identify affected areas and disaster hotspots
5. Provide comprehensive disaster discovery information

When users ask about disasters:
- Delegate historical data queries to bigquery_agent
- Delegate live FEMA data queries to fema_agent
- Use location_finder tools to geocode and locate disasters
- Synthesize location and disaster data into actionable intelligence""",
        tools=[find_disaster_location, geocode_address],
        sub_agents=[bq_agent, fema_agent],
    )
    logger.info("[create_disaster_discovery_agent] Disaster Discovery agent created successfully")
    return disaster_discovery

