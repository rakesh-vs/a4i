"""FastAPI wrapper for First Responder Agent with AG-UI ADK integration."""

import os
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
import uvicorn

from first_responder_agent.agent import root_agent

# Load environment variables
load_dotenv()

# Create ADK Agent wrapper for AG-UI protocol
adk_first_responder = ADKAgent(
    adk_agent=root_agent,
    app_name="first_responder_agent",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(
    title="First Responder Agent API",
    description="Emergency response coordination agent with disaster discovery and relief finder capabilities",
    version="1.0.0"
)

# Add the ADK endpoint at root path for AG-UI protocol
add_adk_fastapi_endpoint(app, adk_first_responder, path="/")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("   Get a key from: https://makersuite.google.com/app/apikey")
        print()

    port = int(os.getenv("PORT", "8000"))
    print(f"🚀 Starting First Responder Agent API on port {port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

