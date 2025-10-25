"""Common BigQuery Data Agent - Shared across multiple agents for various use cases."""

import os
import logging
from typing import Optional
from google.cloud import bigquery
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

logger = logging.getLogger(__name__)


def _get_bigquery_client():
    """Get BigQuery client.

    Raises:
        ValueError: If GCP_PROJECT environment variable is not set
        Exception: If BigQuery client creation fails
    """
    logger.info("[_get_bigquery_client] Attempting to get BigQuery client")
    project_id = os.getenv("GCP_PROJECT")
    if not project_id:
        logger.error("[_get_bigquery_client] GCP_PROJECT environment variable not set")
        raise ValueError("GCP_PROJECT environment variable not set")
    logger.info(f"[_get_bigquery_client] Creating BigQuery client for project: {project_id}")
    try:
        client = bigquery.Client(project=project_id)
        logger.info("[_get_bigquery_client] BigQuery client created successfully")
        return client
    except Exception as e:
        logger.error(f"[_get_bigquery_client] Failed to create BigQuery client: {str(e)}", exc_info=True)
        raise


# ============ ONGOING STORMS QUERIES ============

def get_ongoing_storms_info(lat: float, long: float, radius_miles: float = 25.0) -> dict:
    """Query ongoing storm information by latitude and longitude with proximity search.

    This function queries BigQuery for storm data within a specified radius of the given coordinates.
    It ALWAYS returns a result, even if no storms are found or if an error occurs.

    Args:
        lat: Latitude coordinate in decimal degrees (required, e.g., 40.7128 for New York)
        long: Longitude coordinate in decimal degrees (required, e.g., -74.0060 for New York)
        radius_miles: Search radius in miles (default: 25 miles)

    Returns:
        Dictionary with the following structure:
        - On success: {"status": "success", "latitude": lat, "longitude": long, "count": int, "storms": list}
        - On error: {"status": "error", "error_message": str}

        Note: Empty results (count=0) are considered successful and return status="success"
    """
    logger.info(f"[get_ongoing_storms_info] Querying storm information for lat={lat}, long={long}, radius={radius_miles} miles")
    try:
        client = _get_bigquery_client()
        # Convert miles to approximate degrees (1 degree ≈ 69 miles)
        radius_degrees = radius_miles / 69.0
        lat_min = lat - radius_degrees
        lat_max = lat + radius_degrees
        long_min = long - radius_degrees
        long_max = long + radius_degrees

        query = f"""
        SELECT YEARMONTH, EPISODE_ID, LOCATION_INDEX, AZIMUTH, LOCATION, LATITUDE, LONGITUDE
        FROM `{client.project}`.c4datasetnew.StormLocations
        WHERE LATITUDE BETWEEN {lat_min} AND {lat_max}
          AND LONGITUDE BETWEEN {long_min} AND {long_max}
        ORDER BY LATITUDE, LONGITUDE
        LIMIT 100
        """
        logger.info(f"[get_ongoing_storms_info] Executing BigQuery proximity search for storms within {radius_miles} miles: {query}")
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        logger.info(f"[get_ongoing_storms_info] Successfully retrieved {len(rows)} storm records for lat={lat}, long={long}")
        return {"status": "success", "latitude": lat, "longitude": long, "count": len(rows), "storms": rows}
    except Exception as e:
        logger.error(f"[get_ongoing_storms_info] Error querying storms for lat={lat}, long={long}: {str(e)}", exc_info=True)
        return {
            "status": "info",
            "latitude": lat,
            "longitude": long,
            "message": f"No storms info, continue with other sources"
        }


# ============ SHELTER QUERIES ============

def get_available_shelter_info(lat: float, long: float, min_beds: Optional[int] = 1, onsite_medical_clinic: Optional[str] = None) -> dict:
    """Query available shelter information by latitude and longitude.

    This function queries BigQuery for shelter data at the specified coordinates.
    It ALWAYS returns a result, even if no shelters are found or if an error occurs.

    Args:
        lat: Latitude coordinate in decimal degrees (required, e.g., 40.7128 for New York)
        long: Longitude coordinate in decimal degrees (required, e.g., -74.0060 for New York)
        min_beds: Minimum number of beds required (optional, default: 1)
        onsite_medical_clinic: Filter by onsite medical clinic availability (optional, 'Yes' or 'No')

    Returns:
        Dictionary with the following structure:
        - On success: {"status": "success", "latitude": lat, "longitude": long, "count": int, "shelters": list}
        - On error: {"status": "error", "error_message": str}

        Note: Empty results (count=0) are considered successful and return status="success"
    """
    logger.info(f"[get_available_shelter_info] Querying shelter information for lat={lat}, long={long}, min_beds={min_beds}, onsite_medical_clinic={onsite_medical_clinic}")
    try:
        client = _get_bigquery_client()

        # Build WHERE clause with required and optional filters
        where_conditions = [f"LATITUDE = {lat}", f"LONGITUDE = {long}"]

        if min_beds is not None:
            where_conditions.append(f"NUMBER_OF_BEDS > {min_beds}")
            logger.info(f"[get_available_shelter_info] Added filter: min_beds > {min_beds}")

        if onsite_medical_clinic is not None:
            where_conditions.append(f"ON_SITE_MEDICAL_CLINIC = '{onsite_medical_clinic}'")
            logger.info(f"[get_available_shelter_info] Added filter: onsite_medical_clinic = {onsite_medical_clinic}")

        where_clause = " AND ".join(where_conditions)
        logger.info(f"[get_available_shelter_info] WHERE clause: {where_clause}")

        query = f"""
        SELECT
            NAME, ADDRESS, CITY, STATE, ZIPCODE, WARD, PROVIDER, TYPE, SUBTYPE, STATUS,
            NUMBER_OF_BEDS, ON_SITE_MEDICAL_CLINIC, AGES_SERVED, HOW_TO_ACCESS, LGBTQ_FOCUSED,
            LATITUDE, LONGITUDE
        FROM `{client.project}`.c4datasetnew.Shelter
        WHERE {where_clause}
        """
        logger.info(f"[get_available_shelter_info] Executing BigQuery {query} for shelters")
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        logger.info(f"[get_available_shelter_info] Successfully retrieved {len(rows)} shelter records for lat={lat}, long={long}")
        return {"status": "success", "latitude": lat, "longitude": long, "count": len(rows), "shelters": rows}
    except Exception as e:
        logger.error(f"[get_available_shelter_info] Error querying shelters for lat={lat}, long={long}: {str(e)}", exc_info=True)
        return {
            "status": "info",
            "latitude": lat,
            "longitude": long,
            "message": f"No shelters info, continue with other sources"
        }


# ============ HOSPITAL QUERIES ============

def check_hospital_capacity(hospital_id: str) -> dict:
    """Check capacity and services of a specific hospital (placeholder)."""
    logger.info(f"[check_hospital_capacity] Placeholder called for hospital_id={hospital_id}")
    # Placeholder implementation
    return {"status": "info", "message": "No hospital capacity info, continue with other sources"}


# ============ SUPPLY QUERIES ============

def check_supply_inventory(supply_id: str) -> dict:
    """Check inventory for a specific supply resource (placeholder)."""
    logger.info(f"[check_supply_inventory] Placeholder called for supply_id={supply_id}")
    # Placeholder implementation
    return {"status": "info", "message": "No supply inventory info, continue with other sources"}


def create_big_query_data_agent_tool():
    """Create and return the BigQuery Data agent wrapped as an AgentTool.

    This function creates a BigQuery agent and wraps it as an AgentTool so it can be
    called directly by other agents. The tool always returns control to the calling agent,
    even when errors occur.

    Returns:
        AgentTool: The BigQuery agent wrapped as a tool
    """
    logger.info("[create_big_query_data_agent_tool] Creating BigQuery Data agent tool")

    big_query_agent = Agent(
        name="big_query_data_agent",
        model="gemini-2.5-flash",
        description="Query BigQuery for disaster and relief data including shelters and storms by location coordinates",
        instruction="""You are a BigQuery Data Agent that queries disaster and relief data.

WORKFLOW:
1. Use the appropriate tool based on what data is requested with the provided lat and long coordinates:
   - For storm data: Use the get_ongoing_storms_info tool
   - For shelter data: Use the get_available_shelter_info tool
   - For hospital data: Use the check_hospital_capacity tool
   - For supply data: Use the check_supply_inventory tool

2. If there is any error or no data is found, just return an empty list. Do not stop.

DO NOT ask for clarification or additional input.
""",
        tools=[
            get_available_shelter_info,
            get_ongoing_storms_info,
            check_hospital_capacity,
            check_supply_inventory,
        ],
    )

    # Wrap the agent as an AgentTool with skip_summarization=True
    # This ensures the raw results are passed back without additional LLM processing
    agent_tool = AgentTool(agent=big_query_agent, skip_summarization=True)

    logger.info("[create_big_query_data_agent_tool] BigQuery Data agent tool created successfully")
    return agent_tool

