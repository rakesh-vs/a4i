"""
Starter ADK Agent - A simple example of building an AI agent with Google ADK.
"""

import os
from google.adk.agents import Agent
from google.adk.tools import google_search


def create_search_agent() -> Agent:
    """Create a simple search assistant agent."""
    return Agent(
        name="search_assistant",
        model="gemini-2.5-flash",
        instruction="""You are a helpful search assistant.
        Your job is to help users find information by searching the web when needed.
        Always provide accurate, relevant, and well-organized information.
        If you don't know something, use the search tool to find the answer.""",
        description="An assistant that can search the web to answer questions",
        tools=[google_search],
    )


async def main():
    """Main entry point for the agent."""
    # Create the agent
    agent = create_search_agent()

    # Example query
    query = "What are the latest developments in AI agents?"

    print(f"🤖 Starting ADK Agent Demo")
    print(f"📝 Query: {query}")
    print("-" * 50)

    # Run the agent
    response = await agent.run(query)

    print(f"\n✅ Agent Response:")
    print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
