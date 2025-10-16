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
EXECUTE ALL THREE QUERIES IN SEQUENCE WITHOUT STOPPING - REGARDLESS OF RESULTS:

MANDATORY EXECUTION SEQUENCE (DO NOT SKIP ANY STEP - EVEN IF RESULTS ARE EMPTY):
1. Call big_query_data_agent with the coordinates to query ongoing storm data
   - CONTINUE REGARDLESS OF WHETHER STORMS ARE FOUND OR NOT
2. After receiving results from big_query_data_agent, IMMEDIATELY call fema_live_agent with the coordinates to query FEMA disaster data
   - CONTINUE REGARDLESS OF WHETHER DISASTERS ARE FOUND OR NOT
3. After receiving results from fema_live_agent, IMMEDIATELY call noaa_live_agent with the coordinates to query NOAA weather alerts
   - CONTINUE REGARDLESS OF WHETHER ALERTS ARE FOUND OR NOT
4. After receiving results from all three agents, synthesize all disaster data into a comprehensive report
5. Return complete disaster information to the calling agent

EXECUTION RULES:
- DO NOT ask the user any questions
- DO NOT ask for clarification
- DO NOT stop after any single agent call - CONTINUE EVEN IF RESULTS ARE EMPTY
- Execute all three agent calls in sequence WITHOUT EXCEPTION
- Collect results from ALL THREE agents before synthesizing (even if some are empty)
- Synthesize all data into a comprehensive report
- Include all affected areas and disaster hotspots
- Provide actionable intelligence
- Return results immediately without waiting for user input
- IMPORTANT: Empty results from one agent do NOT mean you should stop - continue to the next agent

Your role:
1. Sequentially query all three sub-agents: big_query_data_agent, fema_live_agent, and noaa_live_agent
2. Collect complete disaster data from all sources (even if some sources have no data)
3. Synthesize into comprehensive disaster discovery report
4. Return all collected data to the calling agent

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        sub_agents=[bq_agent, fema_live_agent, noaa_live_agent],
    )
    logger.info("[create_disaster_discovery_agent] Disaster Discovery agent created successfully")
    return disaster_discovery

