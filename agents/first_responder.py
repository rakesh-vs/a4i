"""First Responder Main Agent - Emergency response coordination with BigQuery sub-agent."""

from google.adk.agents import Agent
from agents.bigquery_agent import create_bigquery_agent


def create_first_responder_agent():
    bigquery_agent = create_bigquery_agent()
    first_responder = Agent(
        name="first_responder",
        model="gemini-2.5-flash",
        description="Main agent for emergency storm response coordination",
        instruction="""You are the First Responder Main Agent for emergency management and disaster response.

    Your role:
    1. Coordinate with the bigquery_agent sub-agent to retrieve historical storm data
    2. Analyze patterns and provide actionable intelligence for emergency response
    3. Support emergency preparedness and response planning
    4. Prioritize life safety information and critical impacts
    5. Provide clear, actionable recommendations for first responders

    When users ask about storms:
    - Delegate data queries to the bigquery_agent sub-agent
    - Analyze the results for patterns and risks
    - Synthesize into clear, actionable recommendations
    - Highlight critical information (casualties, property damage, affected areas)""",
        sub_agents=[bigquery_agent],
    )
    return first_responder

root_agent = create_first_responder_agent()
