"""FastAPI wrapper for First Responder Agent with AG-UI ADK integration."""

import os
import sys
import logging
from pathlib import Path
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
import uvicorn

# Add parent directory to Python path so we can import first_responder_agent
sys.path.insert(0, str(Path(__file__).parent.parent))

from first_responder_agent.agent import root_agent

# Load environment variables
load_dotenv()

# Configure logging to show ALL logs (DEBUG level) and write to file
log_file = Path(__file__).parent.parent / "agent_run.log"

# Remove old log file if it exists
if log_file.exists():
    log_file.unlink()

# Create file handler with immediate flushing
file_handler = logging.FileHandler(log_file, mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, console_handler],
    force=True  # Force reconfiguration even if already configured
)

# Set specific loggers to DEBUG level to see everything
logging.getLogger('first_responder_agent').setLevel(logging.DEBUG)
logging.getLogger('uvicorn.access').setLevel(logging.WARNING)  # Reduce uvicorn noise

print(f"📝 Logging to: {log_file}")
logging.info(f"Logging initialized - writing to {log_file}")

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

