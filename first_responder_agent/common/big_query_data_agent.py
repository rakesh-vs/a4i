"""Common BigQuery Data Agent - Shared across multiple agents for various use cases."""

import os
import logging
from typing import Optional
from google.cloud import bigquery
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def _get_bigquery_client():
    """Get BigQuery client."""
    logger.info("[_get_bigquery_client] Attempting to get BigQuery client")
    project_id = os.getenv("GCP_PROJECT")
    if not project_id:
        logger.error("[_get_bigquery_client] GCP_PROJECT environment variable not set")
        raise ValueError("GCP_PROJECT environment variable not set")
    logger.info(f"[_get_bigquery_client] Creating BigQuery client for project: {project_id}")
    client = bigquery.Client(project=project_id)
    logger.info("[_get_bigquery_client] BigQuery client created successfully")
    return client


# ============ ONGOING STORMS QUERIES ============

def get_ongoing_storms_info(lat: float, long: float, radius_miles: float = 25.0) -> dict:
    """Query ongoing storm information by latitude and longitude with proximity search.

    Args:
        lat: Latitude coordinate (required)
        long: Longitude coordinate (required)
        radius_miles: Search radius in miles (default: 25 miles)

    Returns:
        Dictionary with status and storm results
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
        return {"status": "error", "error_message": f"Failed to query storms: {str(e)}"}


# ============ SHELTER QUERIES ============

def get_available_shelter_info(lat: float, long: float, min_beds: Optional[int] = 1, onsite_medical_clinic: Optional[str] = None) -> dict:
    """Query available shelter information by latitude and longitude.

    Args:
        lat: Latitude coordinate (required)
        long: Longitude coordinate (required)
        min_beds: Minimum number of beds (optional)
        onsite_medical_clinic: Filter by onsite medical clinic availability (optional, 'Yes' or 'No')

    Returns:
        Dictionary with status and shelter results
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
        return {"status": "error", "error_message": f"Failed to query shelters: {str(e)}"}


# ============ HOSPITAL QUERIES ============

def check_hospital_capacity(hospital_id: str) -> dict:
    """Check capacity and services of a specific hospital (placeholder)."""
    logger.info(f"[check_hospital_capacity] Placeholder called for hospital_id={hospital_id}")
    # Placeholder implementation
    return {"status": "placeholder", "message": "Hospital capacity check not yet implemented"}


# ============ SUPPLY QUERIES ============

def check_supply_inventory(supply_id: str) -> dict:
    """Check inventory for a specific supply resource (placeholder)."""
    logger.info(f"[check_supply_inventory] Placeholder called for supply_id={supply_id}")
    # Placeholder implementation
    return {"status": "placeholder", "message": "Supply inventory check not yet implemented"}


def create_big_query_data_agent():
    """Create and return the common BigQuery Data agent."""
    logger.info("[create_big_query_data_agent] Creating common BigQuery Data agent")

    big_query_agent = Agent(
        name="big_query_data_agent",
        model="gemini-2.5-flash",
        description="Common agent for querying BigQuery data for shelters and storms",
        instruction="""You are a common BigQuery Data Agent used by multiple agents for querying disaster and relief data.

CRITICAL: Execute queries IMMEDIATELY without asking for clarification. ALWAYS RETURN RESULTS EVEN IF EMPTY. THEN COMPLETE YOUR TASK.

You have access to tools for:
- Getting available shelter information by location with optional filters
- Getting ongoing storm information by location
- Checking hospital capacity (placeholder)
- Checking supply inventory (placeholder)

EXECUTION RULES:
- Execute queries immediately with the provided coordinates
- Do NOT ask for clarification or additional parameters
- Return all available data for the given location
- Return results in clear, structured format
- Do NOT wait for user input
- IMPORTANT: Always return results to the calling agent, even if no data is found
- Empty results are valid results - return them immediately
- Do NOT stop or ask for clarification if results are empty
- AFTER RETURNING RESULTS, YOUR TASK IS COMPLETE - let the calling agent continue

TASK COMPLETION:
1. Call the appropriate tool with the provided coordinates
2. Receive the results (even if empty)
3. Return the results to the calling agent
4. Your task is now complete - do not ask for more input or clarification

Use these tools to retrieve data from BigQuery. Return clear, structured results. Always return results immediately after querying, regardless of whether data was found or not. Then your task is complete.""",
        tools=[
            get_available_shelter_info,
            get_ongoing_storms_info,
            check_hospital_capacity,
            check_supply_inventory,
        ],
    )
    logger.info("[create_big_query_data_agent] BigQuery Data agent created successfully")
    return big_query_agent

