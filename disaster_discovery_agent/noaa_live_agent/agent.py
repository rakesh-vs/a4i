"""NOAA Live Agent - Queries live NOAA weather and disaster data from NOAA API."""

from typing import Optional
import requests
import logging
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

# NOAA API base URLs
NOAA_WEATHER_API = "https://api.weather.gov"
NOAA_ALERTS_API = "https://api.weather.gov/alerts/active"


def query_active_alerts(state: Optional[str] = None, limit: int = 20) -> dict:
    """Query active weather alerts from NOAA.

    Args:
        state: Optional two-letter state code (e.g., 'TX', 'CA')
        limit: Maximum number of results to return

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_active_alerts] Starting query with state={state}, limit={limit}")
    try:
        url = NOAA_ALERTS_API
        params = {}
        
        if state:
            params["point"] = f"state={state.upper()}"
        
        logger.debug(f"[query_active_alerts] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_active_alerts] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        alerts = data.get("features", [])[:limit]
        logger.info(f"[query_active_alerts] Successfully retrieved {len(alerts)} alerts for state={state}")
        return {
            "status": "success",
            "state": state.upper() if state else "All",
            "count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        logger.error(f"[query_active_alerts] Error querying alerts: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query active alerts: {str(e)}"
        }


def query_weather_alerts_by_type(alert_type: Optional[str] = None, limit: int = 15) -> dict:
    """Query weather alerts by type (e.g., 'Tornado Warning', 'Flood Warning').

    Args:
        alert_type: Type of alert to filter by
        limit: Maximum number of results

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_weather_alerts_by_type] Starting query with alert_type={alert_type}, limit={limit}")
    try:
        url = NOAA_ALERTS_API
        params = {}
        
        if alert_type:
            params["event"] = alert_type
        
        logger.debug(f"[query_weather_alerts_by_type] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_weather_alerts_by_type] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        alerts = data.get("features", [])[:limit]
        logger.info(f"[query_weather_alerts_by_type] Successfully retrieved {len(alerts)} alerts for type={alert_type}")
        return {
            "status": "success",
            "alert_type": alert_type or "All",
            "count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        logger.error(f"[query_weather_alerts_by_type] Error querying alerts by type: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query weather alerts by type: {str(e)}"
        }


def query_severe_weather_outlook(limit: int = 10) -> dict:
    """Query NOAA severe weather outlook and forecasts.

    Args:
        limit: Maximum number of results

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_severe_weather_outlook] Starting query with limit={limit}")
    try:
        url = f"{NOAA_WEATHER_API}/products/types/SWO"
        params = {"limit": limit}
        
        logger.debug(f"[query_severe_weather_outlook] API URL: {url}, params: {params}")
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"[query_severe_weather_outlook] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        outlooks = data.get("@graph", [])[:limit]
        logger.info(f"[query_severe_weather_outlook] Successfully retrieved {len(outlooks)} outlooks")
        return {
            "status": "success",
            "count": len(outlooks),
            "outlooks": outlooks
        }
    except Exception as e:
        logger.error(f"[query_severe_weather_outlook] Error querying outlook: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query severe weather outlook: {str(e)}"
        }


def query_weather_by_location(latitude: float, longitude: float) -> dict:
    """Query weather information for a specific location.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        Dictionary with status and results
    """
    logger.info(f"[query_weather_by_location] Starting query for lat={latitude}, lon={longitude}")
    try:
        url = f"{NOAA_WEATHER_API}/points/{latitude},{longitude}"
        
        logger.debug(f"[query_weather_by_location] API URL: {url}")
        response = requests.get(url, timeout=10)
        logger.debug(f"[query_weather_by_location] Response status code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"[query_weather_by_location] Successfully retrieved weather for location")
        return {
            "status": "success",
            "latitude": latitude,
            "longitude": longitude,
            "weather_data": data
        }
    except Exception as e:
        logger.error(f"[query_weather_by_location] Error querying weather: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": f"Failed to query weather by location: {str(e)}"
        }


def create_noaa_live_agent():
    """Create and return the NOAA Live agent."""
    logger.info("[create_noaa_live_agent] Creating NOAA Live agent with tools")
    noaa_live_agent = Agent(
        name="noaa_live_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for querying live NOAA weather and disaster data",
        instruction="""You are a sub-agent that queries live NOAA weather and disaster data from the NOAA API.
    You have access to tools to:
    - Query active weather alerts by state
    - Query weather alerts by type (Tornado Warning, Flood Warning, etc.)
    - Query severe weather outlooks and forecasts
    - Query weather information for specific locations

    Use these tools to retrieve current NOAA weather and alert data. Return clear, structured results.""",
        tools=[
            query_active_alerts,
            query_weather_alerts_by_type,
            query_severe_weather_outlook,
            query_weather_by_location,
        ],
    )
    logger.info("[create_noaa_live_agent] NOAA Live agent created successfully")
    return noaa_live_agent

