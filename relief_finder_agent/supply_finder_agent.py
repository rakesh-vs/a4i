"""Supply Finder Sub-Agent - Finds available relief supplies."""

import logging
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def find_supplies(supply_type: str, location: str) -> dict:
    """Find available relief supplies.
    
    Args:
        supply_type: Type of supply (e.g., 'water', 'food', 'medical')
        location: Location to search for supplies
        
    Returns:
        Dictionary with supply information
    """
    logger.info(f"[find_supplies] Finding {supply_type} supplies in {location}")
    try:
        return {
            "status": "success",
            "supply_type": supply_type,
            "location": location,
            "supplies": []
        }
    except Exception as e:
        logger.error(f"[find_supplies] Error finding supplies: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to find supplies: {str(e)}"
        }


def check_supply_inventory(supply_id: str) -> dict:
    """Check inventory for a supply resource.
    
    Args:
        supply_id: ID of the supply resource
        
    Returns:
        Dictionary with inventory information
    """
    logger.info(f"[check_supply_inventory] Checking inventory for supply_id={supply_id}")
    try:
        return {
            "status": "success",
            "supply_id": supply_id,
            "inventory": {}
        }
    except Exception as e:
        logger.error(f"[check_supply_inventory] Error checking inventory: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to check supply inventory: {str(e)}"
        }


def create_supply_finder_agent():
    """Create and return the Supply Finder agent."""
    logger.info("[create_supply_finder_agent] Creating Supply Finder agent")
    
    supply_finder = Agent(
        name="supply_finder_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for finding available relief supplies",
        instruction="""You are the Supply Finder Sub-Agent responsible for locating relief supplies.

Your role:
- Find available relief supplies (water, food, medical, etc.)
- Check supply inventory and availability
- Provide supply location and contact information
- Help coordinate supply distribution""",
        tools=[find_supplies, check_supply_inventory],
    )
    logger.info("[create_supply_finder_agent] Supply Finder agent created successfully")
    return supply_finder

