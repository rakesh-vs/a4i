"""FEMA Live Agent - Queries live FEMA data from OpenFEMA API."""

from typing import Optional
import requests
import logging
from google.adk.agents import Agent

# Configure logging
logger = logging.getLogger(__name__)


# FEMA OpenFEMA API base URL
FEMA_API_BASE = "https://www.fema.gov/api/open"


def query_disasters(state: Optional[str] = None, limit: int = 10) -> dict:
    """Query active and recent disasters from FEMA.

    Args:
        state: Optional two-letter state code (e.g., 'TX', 'CA')
        limit: Maximum number of results to return

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_disasters] Starting query with state={state}, limit={limit}")
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$top": limit
        }

        if state:
            params["$filter"] = f"state eq '{state.upper()}'"

        logger.debug(f"[query_disasters] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_disasters] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        disasters = data.get("DisasterDeclarationsSummaries", [])
        logger.info(f"[query_disasters] Successfully retrieved {len(disasters)} disasters for state={state}")
        return {
            "status": "success",
            "state": state.upper() if state else "All",
            "count": len(disasters),
            "disasters": disasters
        }
    except Exception as e:
        logger.error(f"[query_disasters] Error querying disasters: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query disasters: {str(e)}"
        }


def query_disaster_declarations(disaster_type: Optional[str] = None, limit: int = 15) -> dict:
    """Query disaster declarations by type.

    Args:
        disaster_type: Type of disaster (e.g., 'Hurricane', 'Tornado', 'Flood')
        limit: Maximum number of results

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_disaster_declarations] Starting query with disaster_type={disaster_type}, limit={limit}")
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$top": limit
        }

        if disaster_type:
            params["$filter"] = f"incidentType eq '{disaster_type}'"

        logger.debug(f"[query_disaster_declarations] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_disaster_declarations] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        declarations = data.get("DisasterDeclarationsSummaries", [])
        logger.info(f"[query_disaster_declarations] Successfully retrieved {len(declarations)} declarations for type={disaster_type}")
        return {
            "status": "success",
            "disaster_type": disaster_type or "All",
            "count": len(declarations),
            "declarations": declarations
        }
    except Exception as e:
        logger.error(f"[query_disaster_declarations] Error querying declarations: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query disaster declarations: {str(e)}"
        }


def query_fema_assistance(state: Optional[str] = None, limit: int = 20) -> dict:
    """Query FEMA assistance programs and funding.

    Args:
        state: Optional two-letter state code
        limit: Maximum number of results

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_fema_assistance] Starting query with state={state}, limit={limit}")
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$top": limit
        }

        if state:
            params["$filter"] = f"state eq '{state.upper()}'"

        logger.debug(f"[query_fema_assistance] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_fema_assistance] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        summaries = data.get("DisasterDeclarationsSummaries", [])
        logger.info(f"[query_fema_assistance] Successfully retrieved {len(summaries)} assistance programs for state={state}")
        return {
            "status": "success",
            "state": state.upper() if state else "All",
            "count": len(summaries),
            "assistance_programs": summaries
        }
    except Exception as e:
        logger.error(f"[query_fema_assistance] Error querying assistance: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query FEMA assistance: {str(e)}"
        }


def query_disaster_summary(disaster_number: int) -> dict:
    """Get detailed summary for a specific disaster.

    Args:
        disaster_number: FEMA disaster number

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_disaster_summary] Starting query for disaster_number={disaster_number}")
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$filter": f"disasterNumber eq {disaster_number}"
        }

        logger.debug(f"[query_disaster_summary] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_disaster_summary] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        declarations = data.get("DisasterDeclarationsSummaries", [])
        if declarations:
            logger.info(f"[query_disaster_summary] Successfully retrieved summary for disaster_number={disaster_number}")
            return {
                "status": "success",
                "disaster_number": disaster_number,
                "summary": declarations[0]
            }
        else:
            logger.warning(f"[query_disaster_summary] Disaster not found for disaster_number={disaster_number}")
            return {
                "status": "not_found",
                "disaster_number": disaster_number,
                "message": "Disaster not found"
            }
    except Exception as e:
        logger.error(f"[query_disaster_summary] Error querying disaster summary: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query disaster summary: {str(e)}"
        }


def create_fema_live_agent():
    """Create and return the FEMA Live agent."""
    logger.info("[create_fema_live_agent] Creating FEMA Live agent with tools")
    fema_live_agent = Agent(
        name="fema_live_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for querying live FEMA data from OpenFEMA API",
        instruction="""You are a sub-agent that queries live FEMA data from the OpenFEMA API.

CRITICAL: Execute queries IMMEDIATELY without asking for clarification. Return results and let the calling agent continue. THEN COMPLETE YOUR TASK.

You have access to tools to:
    - Query active and recent disasters by state
    - Query disaster declarations by type
    - Query FEMA assistance programs and funding
    - Get detailed summaries for specific disasters

EXECUTION RULES:
- Execute queries immediately with the provided coordinates/location
- Do NOT ask for clarification or additional parameters
- Return all available FEMA disaster data for the given location
- Return results in clear, structured format
- Do NOT wait for user input
- Return results so the calling agent can continue to the next step
- AFTER RETURNING RESULTS, YOUR TASK IS COMPLETE - let the calling agent continue

TASK COMPLETION:
1. Call the appropriate tool with the provided location/coordinates
2. Receive the results (even if empty)
3. Return the results to the calling agent
4. Your task is now complete - do not ask for more input or clarification

Use these tools to retrieve current FEMA disaster and assistance data. Return clear, structured results. Then your task is complete.

## ⚠️ CRITICAL: Control Transfer
**ALWAYS** after completing your task, transfer control to the
calling agent using the transfer_to_agent tool.""",
        tools=[
            query_disasters,
            query_disaster_declarations,
            query_fema_assistance,
            query_disaster_summary,
        ],
    )
    logger.info("[create_fema_live_agent] FEMA Live agent created successfully")

    return fema_live_agent

