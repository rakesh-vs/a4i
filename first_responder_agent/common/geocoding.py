"""Geocoding utility for converting location strings to coordinates."""

import logging
import os
from typing import Optional, Tuple
import requests

logger = logging.getLogger(__name__)


def geocode_location(location: str) -> Optional[Tuple[float, float]]:
    """Convert a location string to latitude and longitude coordinates.
    
    Args:
        location: Location string (e.g., "Sunnyvale, CA", "San Francisco, California")
    
    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    try:
        google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not google_maps_api_key:
            logger.error("[geocode_location] GOOGLE_MAPS_API_KEY not set in environment")
            return None
        
        # Use Google Maps Geocoding API
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location,
            "key": google_maps_api_key
        }
        
        logger.info(f"[geocode_location] Geocoding location: {location}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "OK" and data.get("results"):
            result = data["results"][0]
            lat = result["geometry"]["location"]["lat"]
            lng = result["geometry"]["location"]["lng"]
            logger.info(f"[geocode_location] Successfully geocoded '{location}' to ({lat}, {lng})")
            return (lat, lng)
        else:
            logger.warning(f"[geocode_location] Geocoding failed for '{location}': {data.get('status')}")
            return None
    except Exception as e:
        logger.error(f"[geocode_location] Error geocoding location '{location}': {str(e)}", exc_info=True)
        return None

