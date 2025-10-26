"""Supply Finder Tool - Finds available relief supplies."""

import logging
from typing import Dict, Any
from google.adk.tools import ToolContext
from ..common.search_places_tool import search_nearby_places
from ..common.state_tools import update_agent_activity
from ..common.bigquery_tools import check_supply_inventory

logger = logging.getLogger(__name__)


def find_supplies(
    tool_context: ToolContext,
    latitude: float,
    longitude: float,
    radius: int = 5000
) -> Dict[str, Any]:
    """
    Find available relief supplies near the given coordinates.

    This tool combines BigQuery supply inventory data with Google Maps Places API
    to help locate emergency supplies.

    Args:
        tool_context: The tool context containing state
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in meters (default: 5000)

    Returns:
        Dict with supply search results and summary
    """
    try:
        logger.info(f"[find_supplies] 📦 Starting supply search near ({latitude}, {longitude})")

        # Update agent activity to running
        update_agent_activity(tool_context.state, "supply_finder_agent", "running")

        results = {
            "status": "success",
            "latitude": latitude,
            "longitude": longitude,
            "bigquery_supplies": [],
            "maps_supplies": [],
            "summary": ""
        }

        # Step 1: Query BigQuery for supply inventory data
        logger.info(f"[find_supplies] Step 1: Querying BigQuery for supply inventory")
        try:
            bq_result = check_supply_inventory(f"supply_{latitude}_{longitude}")
            if bq_result.get("status") == "success":
                results["bigquery_supplies"] = bq_result.get("supplies", [])
                logger.info(f"[find_supplies] Found {len(results['bigquery_supplies'])} supplies from BigQuery")
            else:
                logger.info(f"[find_supplies] BigQuery supply query: {bq_result.get('message', 'No data')}")
        except Exception as e:
            logger.error(f"[find_supplies] Error querying BigQuery: {str(e)}")

        # Step 2: Search Google Maps for pharmacies (often have emergency supplies)
        logger.info(f"[find_supplies] Step 2: Searching Google Maps for pharmacies and supply locations")
        try:
            maps_result = search_nearby_places(
                tool_context=tool_context,
                latitude=latitude,
                longitude=longitude,
                place_type="pharmacy",
                radius=radius
            )
            if maps_result.get("status") == "success":
                results["maps_supplies"] = maps_result.get("locations", [])
                logger.info(f"[find_supplies] Found {len(results['maps_supplies'])} supply locations from Google Maps")
            else:
                logger.warning(f"[find_supplies] Google Maps search returned: {maps_result.get('message', 'Unknown error')}")
        except Exception as e:
            logger.error(f"[find_supplies] Error searching Google Maps: {str(e)}")

        # Step 3: Generate summary
        total_supplies = len(results["bigquery_supplies"]) + len(results["maps_supplies"])

        if total_supplies == 0:
            results["summary"] = f"No supply locations found within {radius/1000}km of the location."
        else:
            summary_parts = []
            if results["bigquery_supplies"]:
                summary_parts.append(f"{len(results['bigquery_supplies'])} supplies from emergency database")
            if results["maps_supplies"]:
                summary_parts.append(f"{len(results['maps_supplies'])} pharmacy/supply locations from Google Maps")

            results["summary"] = f"Found {total_supplies} total supply location(s): {' and '.join(summary_parts)}."

        logger.info(f"[find_supplies] ✅ Supply search completed: {results['summary']}")

        # Update agent activity to completed
        update_agent_activity(tool_context.state, "supply_finder_agent", "completed")

        return results

    except Exception as e:
        logger.error(f"[find_supplies] Error in supply search: {str(e)}")
        update_agent_activity(tool_context.state, "supply_finder_agent", "completed")
        return {
            "status": "error",
            "message": f"Error searching for supplies: {str(e)}",
            "latitude": latitude,
            "longitude": longitude
        }
