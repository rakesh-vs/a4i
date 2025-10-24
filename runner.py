"""
Conversational chat runner for the First Responder Agent.
"""
import asyncio
import os
from dotenv import load_dotenv
from vertexai import agent_engines, init

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
PROJECT_ID = os.getenv("GCP_PROJECT")
LOCATION = os.getenv("GCP_REGION", "us-west1")
RESOURCE_NAME = os.getenv("RESOURCE_NAME")
STAGING_BUCKET = os.getenv("STAGING_BUCKET")
USER_ID = os.getenv("USER_ID", "test-user")

# Validate required configuration
if not PROJECT_ID:
    raise ValueError("GCP_PROJECT environment variable is required")
if not RESOURCE_NAME:
    raise ValueError("RESOURCE_NAME environment variable is required")
if not STAGING_BUCKET:
    raise ValueError("STAGING_BUCKET environment variable is required")

init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

agent_engine = agent_engines.get(RESOURCE_NAME)
session = agent_engine.create_session(user_id=USER_ID)


async def stream_response(message: str):
    """Stream and display agent response."""
    print(f"\n🤖 Agent: ", end="", flush=True)
    full_response = ""

    async for event in agent_engine.async_stream_query(
        user_id=USER_ID,
        session_id=session['id'],
        message=message,
    ):
        # Extract text from event and print it
        if hasattr(event, 'text'):
            text = event.text
            print(text, end="", flush=True)
            full_response += text
        elif isinstance(event, dict) and 'text' in event:
            text = event['text']
            print(text, end="", flush=True)
            full_response += text
        elif isinstance(event, str):
            print(event, end="", flush=True)
            full_response += event

    print()  # New line after response
    return full_response


async def main():
    """Run conversational chat loop with the First Responder Agent."""
    print("=" * 60)
    print("🚨 First Responder Agent - Emergency Response System")
    print("=" * 60)
    print("Chat with the agent about emergency situations and disasters.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break

            # Stream the response
            await stream_response(user_input)

        except KeyboardInterrupt:
            print("\n\n👋 Conversation ended.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())