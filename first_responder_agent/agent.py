"""First Responder Main Agent - Emergency response coordination with BigQuery and FEMA sub-agents."""

from google.adk.agents import Agent
from storm_events_agent.agent import create_bigquery_agent
from fema_agent.agent import create_fema_agent


def create_first_responder_agent():
    bigquery_agent = create_bigquery_agent()
    fema_agent = create_fema_agent()
    first_responder = Agent(
        name="first_responder",
        model="gemini-2.5-flash",
        description="Main agent for emergency storm response coordination",
        instruction="""You are the First Responder Main Agent for emergency management and disaster response.

    Your role:
    1. Coordinate with the bigquery_agent sub-agent to retrieve historical storm data
    2. Coordinate with the fema_agent sub-agent to retrieve live FEMA disaster data
    3. Analyze patterns and provide actionable intelligence for emergency response
    4. Support emergency preparedness and response planning
    5. Prioritize life safety information and critical impacts
    6. Provide clear, actionable recommendations for first responders

    When users ask about storms or disasters:
    - Delegate historical data queries to the bigquery_agent sub-agent
    - Delegate live FEMA data queries to the fema_agent sub-agent
    - Analyze the results for patterns and risks
    - Synthesize into clear, actionable recommendations
    - Highlight critical information (casualties, property damage, affected areas)""",
        sub_agents=[bigquery_agent, fema_agent],
    )
    return first_responder

root_agent = create_first_responder_agent()
