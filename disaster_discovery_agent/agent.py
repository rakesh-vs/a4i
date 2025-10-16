"""Disaster Discovery Agent - Discovers and locates disasters using BigQuery, FEMA, and NOAA data."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from disaster_discovery_agent.fema_agent.agent import create_fema_agent
from disaster_discovery_agent.noaa_agent.agent import create_noaa_agent

logger = logging.getLogger(__name__)


def create_disaster_discovery_agent():
    """Create and return the Disaster Discovery agent."""
    logger.info("[create_disaster_discovery_agent] Creating Disaster Discovery agent")

    # Create sub-agents
    bq_agent = create_big_query_data_agent()
    fema_agent = create_fema_agent()
    noaa_agent = create_noaa_agent()

    disaster_discovery = Agent(
        name="disaster_discovery_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for discovering and locating disasters",
        instruction="""You are the Disaster Discovery Sub-Agent responsible for finding and locating disasters.

Your role:
1. Query historical storm data from the big_query_data_agent sub-agent
2. Query live FEMA disaster data from the fema_agent sub-agent
3. Query live NOAA weather alerts and data from the noaa_agent sub-agent
4. Identify affected areas and disaster hotspots
5. Provide comprehensive disaster discovery information

When users ask about disasters:
- Delegate historical data queries to big_query_data_agent
- Delegate live FEMA data queries to fema_agent
- Delegate live NOAA weather data queries to noaa_agent
- Synthesize disaster data into actionable intelligence""",
        sub_agents=[bq_agent, fema_agent, noaa_agent],
    )
    logger.info("[create_disaster_discovery_agent] Disaster Discovery agent created successfully")
    return disaster_discovery

