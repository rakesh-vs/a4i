"""FEMA agent for querying live FEMA data from OpenFEMA API."""

import requests
from google.adk.agents import Agent


# FEMA OpenFEMA API base URL
FEMA_API_BASE = "https://www.fema.gov/api/open"


def query_disasters(state: str = None, limit: int = 10) -> dict:
    """Query active and recent disasters from FEMA.
    
    Args:
        state: Optional two-letter state code (e.g., 'TX', 'CA')
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with status and results
    """
    try:
        url = f"{FEMA_API_BASE}/v2/disasters"
        params = {
            "$top": limit,
            "$orderby": "declarationDate DESC"
        }
        
        if state:
            params["$filter"] = f"state eq '{state.upper()}'"
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        disasters = data.get("DisasterDeclarations", [])
        return {
            "status": "success",
            "state": state.upper() if state else "All",
            "count": len(disasters),
            "disasters": disasters
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query disasters: {str(e)}"
        }


def query_disaster_declarations(disaster_type: str = None, limit: int = 15) -> dict:
    """Query disaster declarations by type.
    
    Args:
        disaster_type: Type of disaster (e.g., 'Hurricane', 'Tornado', 'Flood')
        limit: Maximum number of results
        
    Returns:
        Dictionary with status and results
    """
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$top": limit,
            "$orderby": "declarationDate DESC"
        }
        
        if disaster_type:
            params["$filter"] = f"contains(incidentType, '{disaster_type}')"
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        declarations = data.get("DisasterDeclarationsSummaries", [])
        return {
            "status": "success",
            "disaster_type": disaster_type or "All",
            "count": len(declarations),
            "declarations": declarations
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query disaster declarations: {str(e)}"
        }


def query_fema_assistance(state: str = None, limit: int = 20) -> dict:
    """Query FEMA assistance programs and funding.
    
    Args:
        state: Optional two-letter state code
        limit: Maximum number of results
        
    Returns:
        Dictionary with status and results
    """
    try:
        url = f"{FEMA_API_BASE}/v2/FemaWebDisasterSummaries"
        params = {
            "$top": limit,
            "$orderby": "declarationDate DESC"
        }
        
        if state:
            params["$filter"] = f"state eq '{state.upper()}'"
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        summaries = data.get("FemaWebDisasterSummaries", [])
        return {
            "status": "success",
            "state": state.upper() if state else "All",
            "count": len(summaries),
            "assistance_programs": summaries
        }
    except Exception as e:
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
    try:
        url = f"{FEMA_API_BASE}/v2/DisasterDeclarationsSummaries"
        params = {
            "$filter": f"disasterNumber eq {disaster_number}"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        declarations = data.get("DisasterDeclarationsSummaries", [])
        if declarations:
            return {
                "status": "success",
                "disaster_number": disaster_number,
                "summary": declarations[0]
            }
        else:
            return {
                "status": "not_found",
                "disaster_number": disaster_number,
                "message": "Disaster not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query disaster summary: {str(e)}"
        }


def create_fema_agent():
    """Create and return the FEMA agent."""
    fema_agent = Agent(
        name="fema_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for querying live FEMA data from OpenFEMA API",
        instruction="""You are a sub-agent that queries live FEMA data from the OpenFEMA API.
    You have access to tools to:
    - Query active and recent disasters by state
    - Query disaster declarations by type
    - Query FEMA assistance programs and funding
    - Get detailed summaries for specific disasters

    Use these tools to retrieve current FEMA disaster and assistance data. Return clear, structured results.""",
        tools=[
            query_disasters,
            query_disaster_declarations,
            query_fema_assistance,
            query_disaster_summary,
        ],
    )

    return fema_agent

