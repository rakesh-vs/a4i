"""Disaster Discovery Agent - Discovers and locates disasters using BigQuery, FEMA Live, and NOAA Live data."""

import logging
from google.adk.agents import Agent
from common.big_query_data_agent import create_big_query_data_agent
from disaster_discovery_agent.fema_live_agent.agent import create_fema_live_agent
from disaster_discovery_agent.noaa_live_agent.agent import create_noaa_live_agent

logger = logging.getLogger(__name__)


def create_disaster_discovery_agent():
    """Create and return the Disaster Discovery agent."""
    logger.info("[create_disaster_discovery_agent] Creating Disaster Discovery agent")

    # Create sub-agents
    bq_agent = create_big_query_data_agent()
    fema_live_agent = create_fema_live_agent()
    noaa_live_agent = create_noaa_live_agent()

    disaster_discovery = Agent(
        name="disaster_discovery_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for discovering and locating disasters",
        instruction="""You are the Disaster Discovery Sub-Agent responsible for finding and locating disasters.

CRITICAL: You will receive coordinates (latitude, longitude) from the first_responder_agent.
EXECUTE IMMEDIATELY WITHOUT ASKING QUESTIONS:

AUTOMATIC EXECUTION SEQUENCE:
1. IMMEDIATELY query historical storm data from big_query_data_agent using the provided coordinates
2. IMMEDIATELY query live FEMA disaster data from fema_live_agent for the location
3. IMMEDIATELY query live NOAA weather alerts from noaa_live_agent for the location
4. Synthesize all disaster data into a comprehensive report
5. Return complete disaster information to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- Execute all queries automatically with the provided coordinates
- Synthesize all data into a comprehensive report
- Include all affected areas and disaster hotspots
- Provide actionable intelligence
- Return results immediately without waiting for user input

Your role:
1. Query historical storm data from the big_query_data_agent sub-agent
2. Query live FEMA disaster data from the fema_live_agent sub-agent
3. Query live NOAA weather alerts and data from the noaa_live_agent sub-agent
4. Identify affected areas and disaster hotspots
5. Provide comprehensive disaster discovery information""",
        sub_agents=[bq_agent, fema_live_agent, noaa_live_agent],
    )
    logger.info("[create_disaster_discovery_agent] Disaster Discovery agent created successfully")
    return disaster_discovery

