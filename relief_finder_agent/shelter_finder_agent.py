"""Shelter Finder Sub-Agent - Finds available shelters."""

import logging
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def find_shelters(location: str, capacity: int = 0) -> dict:
    """Find available shelters in a location.
    
    Args:
        location: Location to search for shelters
        capacity: Minimum capacity required
        
    Returns:
        Dictionary with shelter information
    """
    logger.info(f"[find_shelters] Finding shelters in {location} with capacity >= {capacity}")
    try:
        return {
            "status": "success",
            "location": location,
            "shelters": []
        }
    except Exception as e:
        logger.error(f"[find_shelters] Error finding shelters: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to find shelters: {str(e)}"
        }


def create_shelter_finder_agent():
    """Create and return the Shelter Finder agent."""
    logger.info("[create_shelter_finder_agent] Creating Shelter Finder agent")
    
    shelter_finder = Agent(
        name="shelter_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available shelters",
        instruction="""You are the Shelter Finder Sub-Agent responsible for locating available shelters.

Your role:
- Find available shelters in affected areas
- Check shelter capacity and availability
- Provide shelter location and contact information
- Help coordinate shelter resources""",
        tools=[find_shelters],
    )
    logger.info("[create_shelter_finder_agent] Shelter Finder agent created successfully")
    return shelter_finder

