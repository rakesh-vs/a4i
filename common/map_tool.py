"""Common Map Tool - Shared across multiple agents for displaying various map types."""

import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


# ============ NEARBY LOCATION FINDERS ============

def find_nearby_shelters(center_location: str, radius_km: float = 10) -> dict:
    """Find nearby shelters within a specified radius.
    
    Args:
        center_location: Center location for search
        radius_km: Search radius in kilometers
        
    Returns:
        Dictionary with nearby shelters
    """
    logger.info(f"[find_nearby_shelters] Finding shelters within {radius_km}km of {center_location}")
    try:
        return {
            "status": "success",
            "center_location": center_location,
            "radius_km": radius_km,
            "shelters": []
        }
    except Exception as e:
        logger.error(f"[find_nearby_shelters] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to find nearby shelters: {str(e)}"}


def find_nearby_hospitals(center_location: str, radius_km: float = 10) -> dict:
    """Find nearby hospitals within a specified radius.
    
    Args:
        center_location: Center location for search
        radius_km: Search radius in kilometers
        
    Returns:
        Dictionary with nearby hospitals
    """
    logger.info(f"[find_nearby_hospitals] Finding hospitals within {radius_km}km of {center_location}")
    try:
        return {
            "status": "success",
            "center_location": center_location,
            "radius_km": radius_km,
            "hospitals": []
        }
    except Exception as e:
        logger.error(f"[find_nearby_hospitals] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to find nearby hospitals: {str(e)}"}


def find_nearby_supplies(center_location: str, supply_type: str, radius_km: float = 10) -> dict:
    """Find nearby supply locations within a specified radius.
    
    Args:
        center_location: Center location for search
        supply_type: Type of supply to search for
        radius_km: Search radius in kilometers
        
    Returns:
        Dictionary with nearby supplies
    """
    logger.info(f"[find_nearby_supplies] Finding {supply_type} supplies within {radius_km}km of {center_location}")
    try:
        return {
            "status": "success",
            "center_location": center_location,
            "supply_type": supply_type,
            "radius_km": radius_km,
            "supplies": []
        }
    except Exception as e:
        logger.error(f"[find_nearby_supplies] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to find nearby supplies: {str(e)}"}


# ============ MAP DISPLAY FUNCTIONS ============

def display_disaster_map(disasters: List[Dict[str, Any]], center_location: Optional[str] = None) -> dict:
    """Display disasters on a map.
    
    Args:
        disasters: List of disaster data to display
        center_location: Optional center location for the map
        
    Returns:
        Dictionary with map display information
    """
    logger.info(f"[display_disaster_map] Displaying {len(disasters)} disasters on map")
    try:
        return {
            "status": "success",
            "map_type": "disaster_map",
            "disaster_count": len(disasters),
            "center_location": center_location,
            "map_url": None,
            "disasters": disasters
        }
    except Exception as e:
        logger.error(f"[display_disaster_map] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to display disaster map: {str(e)}"}


def display_relief_resources_map(resources: Dict[str, List[Dict[str, Any]]], center_location: Optional[str] = None) -> dict:
    """Display relief resources on a map.
    
    Args:
        resources: Dictionary of resource types and their locations
        center_location: Optional center location for the map
        
    Returns:
        Dictionary with map display information
    """
    logger.info(f"[display_relief_resources_map] Displaying relief resources on map")
    try:
        return {
            "status": "success",
            "map_type": "relief_resources_map",
            "resource_types": list(resources.keys()),
            "center_location": center_location,
            "map_url": None,
            "resources": resources
        }
    except Exception as e:
        logger.error(f"[display_relief_resources_map] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to display relief resources map: {str(e)}"}


def display_combined_map(disasters: List[Dict[str, Any]], resources: Dict[str, List[Dict[str, Any]]], center_location: Optional[str] = None) -> dict:
    """Display both disasters and relief resources on a combined map.
    
    Args:
        disasters: List of disaster data
        resources: Dictionary of resource types and their locations
        center_location: Optional center location for the map
        
    Returns:
        Dictionary with map display information
    """
    logger.info(f"[display_combined_map] Displaying combined disaster and relief map")
    try:
        return {
            "status": "success",
            "map_type": "combined_map",
            "disaster_count": len(disasters),
            "resource_types": list(resources.keys()),
            "center_location": center_location,
            "map_url": None,
            "disasters": disasters,
            "resources": resources
        }
    except Exception as e:
        logger.error(f"[display_combined_map] Error: {str(e)}", exc_info=True)
        return {"status": "error", "error_message": f"Failed to display combined map: {str(e)}"}

