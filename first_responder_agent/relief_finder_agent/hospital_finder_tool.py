"""Hospital Finder Tool - Finds available hospitals and medical facilities."""

import logging
from typing import Dict, Any
from google.adk.tools import ToolContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import check_hospital_capacity

logger = logging.getLogger(__name__)


def find_hospitals(
    tool_context: ToolContext,
    latitude: float,
    longitude: float,
    radius: int = 5000
) -> Dict[str, Any]:
    """
    Find available hospitals and medical facilities near the given coordinates.

    This tool combines BigQuery hospital data with Google Maps Places API
    to provide comprehensive medical facility information.

    Args:
        tool_context: The tool context containing state
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in meters (default: 5000)

    Returns:
        Dict with hospital search results and summary
    """
    try:
        logger.info(f"[find_hospitals] 🏥 Starting hospital search near ({latitude}, {longitude})")

        # Update agent activity to running
        update_agent_activity(tool_context.state, "hospital_finder_agent", "running")

        results = {
            "status": "success",
            "latitude": latitude,
            "longitude": longitude,
            "bigquery_hospitals": [],
            "maps_hospitals": [],
            "summary": ""
        }

        # Step 1: Query BigQuery for hospital capacity data
        logger.info(f"[find_hospitals] Step 1: Querying BigQuery for hospital data")
        try:
            bq_result = check_hospital_capacity(f"hospital_{latitude}_{longitude}")
            if bq_result.get("status") == "success":
                results["bigquery_hospitals"] = bq_result.get("hospitals", [])
                logger.info(f"[find_hospitals] Found {len(results['bigquery_hospitals'])} hospitals from BigQuery")
            else:
                logger.info(f"[find_hospitals] BigQuery hospital query: {bq_result.get('message', 'No data')}")
        except Exception as e:
            logger.error(f"[find_hospitals] Error querying BigQuery: {str(e)}")

        # Step 2: Search Google Maps for hospitals
        logger.info(f"[find_hospitals] Step 2: Searching Google Maps for hospitals")
        try:
            maps_result = search_nearby_places(
                tool_context=tool_context,
                latitude=latitude,
                longitude=longitude,
                place_type="hospital",
                radius=radius
            )
            if maps_result.get("status") == "success":
                results["maps_hospitals"] = maps_result.get("locations", [])
                logger.info(f"[find_hospitals] Found {len(results['maps_hospitals'])} hospitals from Google Maps")
            else:
                logger.warning(f"[find_hospitals] Google Maps search returned: {maps_result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"[find_hospitals] Error searching Google Maps: {str(e)}")

        # Step 3: Generate summary
        total_hospitals = len(results["bigquery_hospitals"]) + len(results["maps_hospitals"])

        if total_hospitals == 0:
            results["summary"] = f"No hospitals found within {radius/1000}km of the location."
        else:
            summary_parts = []
            if results["bigquery_hospitals"]:
                summary_parts.append(f"{len(results['bigquery_hospitals'])} hospitals from emergency database")
            if results["maps_hospitals"]:
                summary_parts.append(f"{len(results['maps_hospitals'])} hospitals from Google Maps")

            results["summary"] = f"Found {total_hospitals} total hospital(s): {' and '.join(summary_parts)}."

        logger.info(f"[find_hospitals] ✅ Hospital search completed: {results['summary']}")

        # Update agent activity to completed
        update_agent_activity(tool_context.state, "hospital_finder_agent", "completed")

        return results

    except Exception as e:
        logger.error(f"[find_hospitals] Error in hospital search: {str(e)}")
        update_agent_activity(tool_context.state, "hospital_finder_agent", "completed")
        return {
            "status": "error",
            "message": f"Error searching for hospitals: {str(e)}",
            "latitude": latitude,
            "longitude": longitude
        }
