"""Search places tool that automatically updates map state."""

import logging
import os
import googlemaps
from typing import Dict, Any
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

# Initialize Google Maps client
gmaps_client = None


def get_gmaps_client():
    """Get or create Google Maps client."""
    global gmaps_client
    if gmaps_client is None:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            logger.warning("[get_gmaps_client] GOOGLE_MAPS_API_KEY not set")
            return None
        gmaps_client = googlemaps.Client(key=api_key)
    return gmaps_client


def search_nearby_places(
    tool_context: ToolContext,
    latitude: float,
    longitude: float,
    place_type: str,
    radius: int = 5000
) -> Dict[str, Any]:
    """
    Search for nearby places and automatically update the map state.
    
    Args:
        tool_context: The tool context containing state
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        place_type: Type of place (hospital, shelter, pharmacy, etc.)
        radius: Search radius in meters (default: 5000)
    
    Returns:
        Dict with search results
    """
    try:
        logger.info(f"[search_nearby_places] Searching for {place_type} near ({latitude}, {longitude})")
        
        gmaps = get_gmaps_client()
        if not gmaps:
            return {
                "status": "error",
                "message": "Google Maps API key not configured"
            }
        
        # Map place types to Google Places API types
        type_mapping = {
            "hospital": "hospital",
            "shelter": "lodging",
            "emergency": "hospital",
            "medical": "hospital",
            "police": "police",
            "fire_station": "fire_station",
            "pharmacy": "pharmacy",
            "food": "restaurant",
            "supplies": "store"
        }
        
        search_type = type_mapping.get(place_type.lower(), "hospital")
        
        # Search for nearby places
        places_result = gmaps.places_nearby(
            location={"lat": latitude, "lng": longitude},
            radius=radius,
            type=search_type
        )
        
        locations = []
        for place in places_result.get('results', [])[:10]:  # Limit to 10 results
            location_data = {
                "name": place.get('name', 'Unknown'),
                "address": place.get('vicinity', 'Address not available'),
                "lat": place['geometry']['location']['lat'],
                "lng": place['geometry']['location']['lng'],
                "place_id": place.get('place_id', ''),
                "place_type": place_type,
                "rating": place.get('rating', 'N/A'),
                "is_open": place.get('opening_hours', {}).get('open_now', None)
            }
            locations.append(location_data)
        
        # Update map state automatically
        if "locations" not in tool_context.state:
            tool_context.state["locations"] = []
        
        # Append new locations to existing ones
        existing_locations = tool_context.state["locations"]
        tool_context.state["locations"] = existing_locations + locations
        
        # Update center
        tool_context.state["center"] = {
            "lat": latitude,
            "lng": longitude
        }
        
        logger.info(f"[search_nearby_places] Found {len(locations)} locations, updated map state")
        
        return {
            "status": "success",
            "message": f"Found {len(locations)} {place_type}(s)",
            "locations": locations,
            "total_on_map": len(tool_context.state["locations"])
        }
        
    except Exception as e:
        logger.error(f"[search_nearby_places] Error: {str(e)}")
        return {
            "status": "error",
            "message": f"Error searching places: {str(e)}"
        }

