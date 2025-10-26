"""State management tools for updating UI state."""

import logging
from typing import List, Dict, Any, Optional
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)


def update_map_state(
    tool_context: ToolContext,
    locations: List[Dict[str, Any]],
    center: Optional[Dict[str, float]] = None
) -> Dict[str, str]:
    """
    Update the map with new locations/markers.
    
    Args:
        tool_context: The tool context containing state
        locations: List of location objects with name, address, lat, lng, place_id, place_type
        center: Optional center coordinates {lat, lng}
    
    Returns:
        Dict indicating success status
    """
    try:
        logger.info(f"[update_map_state] Updating map with {len(locations)} locations")
        tool_context.state["locations"] = locations
        
        if center:
            tool_context.state["center"] = center
            logger.info(f"[update_map_state] Updated center to {center}")
        
        return {
            "status": "success",
            "message": f"Updated map with {len(locations)} locations"
        }
    except Exception as e:
        logger.error(f"[update_map_state] Error updating map: {str(e)}")
        return {
            "status": "error",
            "message": f"Error updating map: {str(e)}"
        }


def update_agent_activity(
    state: Dict[str, Any],
    current_agent: str,
    status: str = "running"
) -> None:
    """
    Update the current agent activity status.

    Args:
        state: The state dictionary (from callback_context.state)
        current_agent: Name of the currently active agent
        status: Status of the agent ("running" or "completed")
    """
    import time

    try:
        logger.info(f"[update_agent_activity] Agent: {current_agent}, Status: {status}")

        # Initialize activity history if it doesn't exist
        if "activityHistory" not in state:
            state["activityHistory"] = []

        # Update current agent
        state["currentAgent"] = current_agent if status == "running" else None

        # Add to activity history with proper timestamp
        timestamp = int(time.time() * 1000)  # milliseconds
        activity_entry = {
            "agent": current_agent,
            "timestamp": timestamp,
            "status": status
        }

        # Update or add activity in history
        history = state["activityHistory"]

        if status == "completed":
            # Find the most recent running entry for this agent and update it
            for i in range(len(history) - 1, -1, -1):
                if history[i]["agent"] == current_agent:
                    history[i] = activity_entry
                    break
            else:
                # If not found, add new entry
                history.append(activity_entry)
        else:
            # For running status, just append
            history.append(activity_entry)

        # Keep all activities (no limit)
        state["activityHistory"] = history

    except Exception as e:
        logger.error(f"[update_agent_activity] Error: {str(e)}")

