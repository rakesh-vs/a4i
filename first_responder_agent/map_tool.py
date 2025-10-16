"""Map tool for displaying disaster and relief data on maps."""

import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


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
            "map_url": None,  # Would be populated with actual map URL
            "disasters": disasters
        }
    except Exception as e:
        logger.error(f"[display_disaster_map] Error displaying map: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to display disaster map: {str(e)}"
        }


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
            "map_url": None,  # Would be populated with actual map URL
            "resources": resources
        }
    except Exception as e:
        logger.error(f"[display_relief_resources_map] Error displaying map: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to display relief resources map: {str(e)}"
        }


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
            "map_url": None,  # Would be populated with actual map URL
            "disasters": disasters,
            "resources": resources
        }
    except Exception as e:
        logger.error(f"[display_combined_map] Error displaying map: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to display combined map: {str(e)}"
        }

