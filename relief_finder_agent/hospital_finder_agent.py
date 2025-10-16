"""Hospital Finder Sub-Agent - Finds available hospitals and medical facilities."""

import logging
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def find_hospitals(location: str, specialty: str = None) -> dict:
    """Find available hospitals in a location.
    
    Args:
        location: Location to search for hospitals
        specialty: Optional medical specialty to filter by
        
    Returns:
        Dictionary with hospital information
    """
    logger.info(f"[find_hospitals] Finding hospitals in {location}, specialty={specialty}")
    try:
        return {
            "status": "success",
            "location": location,
            "hospitals": []
        }
    except Exception as e:
        logger.error(f"[find_hospitals] Error finding hospitals: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to find hospitals: {str(e)}"
        }


def check_hospital_capacity(hospital_id: str) -> dict:
    """Check available capacity at a hospital.
    
    Args:
        hospital_id: ID of the hospital
        
    Returns:
        Dictionary with capacity information
    """
    logger.info(f"[check_hospital_capacity] Checking capacity for hospital_id={hospital_id}")
    try:
        return {
            "status": "success",
            "hospital_id": hospital_id,
            "capacity": {}
        }
    except Exception as e:
        logger.error(f"[check_hospital_capacity] Error checking capacity: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to check hospital capacity: {str(e)}"
        }


def create_hospital_finder_agent():
    """Create and return the Hospital Finder agent."""
    logger.info("[create_hospital_finder_agent] Creating Hospital Finder agent")
    
    hospital_finder = Agent(
        name="hospital_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available hospitals and medical facilities",
        instruction="""You are the Hospital Finder Sub-Agent responsible for locating medical facilities.

Your role:
- Find available hospitals in affected areas
- Check hospital capacity and available services
- Provide hospital location and contact information
- Help coordinate medical resources""",
        tools=[find_hospitals, check_hospital_capacity],
    )
    logger.info("[create_hospital_finder_agent] Hospital Finder agent created successfully")
    return hospital_finder

