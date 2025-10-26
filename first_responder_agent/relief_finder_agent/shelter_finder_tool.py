"""Shelter Finder Tool - Finds available shelters."""

import logging
from typing import Dict, Any
from google.adk.tools import ToolContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import get_available_shelter_info as bq_get_shelter_info

logger = logging.getLogger(__name__)


def find_shelters(
    tool_context: ToolContext,
    latitude: float,
    longitude: float,
    radius: int = 5000
) -> Dict[str, Any]:
    """
    Find available shelters near the given coordinates.

    This tool combines BigQuery shelter data with Google Maps Places API
    to provide comprehensive shelter information.

    Args:
        tool_context: The tool context containing state
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in meters (default: 5000)

    Returns:
        Dict with shelter search results and summary
    """
    try:
        logger.info(f"[find_shelters] 🏠 Starting shelter search near ({latitude}, {longitude})")

        # Update agent activity to running
        update_agent_activity(tool_context.state, "shelter_finder_agent", "running")

        results = {
            "status": "success",
            "latitude": latitude,
            "longitude": longitude,
            "bigquery_shelters": [],
            "maps_shelters": [],
            "summary": ""
        }

        # Step 1: Query BigQuery for shelter data
        logger.info(f"[find_shelters] Step 1: Querying BigQuery for shelter data")
        try:
            bq_result = bq_get_shelter_info(latitude, longitude)
            if bq_result.get("status") == "success":
                results["bigquery_shelters"] = bq_result.get("shelters", [])
                logger.info(f"[find_shelters] Found {len(results['bigquery_shelters'])} shelters from BigQuery")
            else:
                logger.warning(f"[find_shelters] BigQuery shelter query returned: {bq_result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"[find_shelters] Error querying BigQuery: {str(e)}")

        # Step 2: Search Google Maps for shelters
        logger.info(f"[find_shelters] Step 2: Searching Google Maps for shelters")
        try:
            maps_result = search_nearby_places(
                tool_context=tool_context,
                latitude=latitude,
                longitude=longitude,
                place_type="shelter",
                radius=radius
            )
            if maps_result.get("status") == "success":
                results["maps_shelters"] = maps_result.get("locations", [])
                logger.info(f"[find_shelters] Found {len(results['maps_shelters'])} shelters from Google Maps")
            else:
                logger.warning(f"[find_shelters] Google Maps search returned: {maps_result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"[find_shelters] Error searching Google Maps: {str(e)}")

        # Step 3: Generate summary
        total_shelters = len(results["bigquery_shelters"]) + len(results["maps_shelters"])

        if total_shelters == 0:
            results["summary"] = f"No shelters found within {radius/1000}km of the location."
        else:
            summary_parts = []
            if results["bigquery_shelters"]:
                summary_parts.append(f"{len(results['bigquery_shelters'])} shelters from emergency database")
            if results["maps_shelters"]:
                summary_parts.append(f"{len(results['maps_shelters'])} lodging facilities from Google Maps")

            results["summary"] = f"Found {total_shelters} total shelter options: {' and '.join(summary_parts)}."

        logger.info(f"[find_shelters] ✅ Shelter search completed: {results['summary']}")

        # Update agent activity to completed
        update_agent_activity(tool_context.state, "shelter_finder_agent", "completed")

        return results

    except Exception as e:
        logger.error(f"[find_shelters] Error in shelter search: {str(e)}")
        update_agent_activity(tool_context.state, "shelter_finder_agent", "completed")
        return {
            "status": "error",
            "message": f"Error searching for shelters: {str(e)}",
            "latitude": latitude,
            "longitude": longitude
        }

