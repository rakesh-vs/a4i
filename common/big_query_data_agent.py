"""Common BigQuery Data Agent - Shared across multiple agents for various use cases."""

import os
import logging
from typing import Optional
from google.cloud import bigquery
from google.adk.agents import Agent

logger = logging.getLogger(__name__)


def _get_bigquery_client():
    """Get BigQuery client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return bigquery.Client(project=project_id)


# ============ ONGOING STORMS QUERIES ============

def get_ongoing_storms_info(lat: float, long: float) -> dict:
    """Query ongoing storm information by latitude and longitude.

    Args:
        lat: Latitude coordinate (required)
        long: Longitude coordinate (required)

    Returns:
        Dictionary with status and storm results
    """
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT YEARMONTH, EPISODE_ID, LOCATION_INDEX, RANGE, AZIMUTH, LOCATION, LATITUDE, LONGITUDE
        FROM qwiklabs-gcp-00-fb4bb5fddc00.c4datasetnew.StormLocations
        WHERE LATITUDE = {lat} AND LONGITUDE = {long}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "latitude": lat, "longitude": long, "count": len(rows), "storms": rows}
    except Exception as e:
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
    try:
        client = _get_bigquery_client()

        # Build WHERE clause with required and optional filters
        where_conditions = [f"LATITUDE = {lat}", f"LONGITUDE = {long}"]

        if min_beds is not None:
            where_conditions.append(f"NUMBER_OF_BEDS > {min_beds}")

        if onsite_medical_clinic is not None:
            where_conditions.append(f"ON_SITE_MEDICAL_CLINIC = '{onsite_medical_clinic}'")

        where_clause = " AND ".join(where_conditions)

        query = f"""
        SELECT
            NAME, ADDRESS, CITY, STATE, ZIPCODE, WARD, PROVIDER, TYPE, SUBTYPE, STATUS,
            NUMBER_OF_BEDS, ON_SITE_MEDICAL_CLINIC, AGES_SERVED, HOW_TO_ACCESS, LGBTQ_FOCUSED,
            LATITUDE, LONGITUDE
        FROM qwiklabs-gcp-00-fb4bb5fddc00.c4datasetnew.Shelter
        WHERE {where_clause}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "latitude": lat, "longitude": long, "count": len(rows), "shelters": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query shelters: {str(e)}"}


# ============ HOSPITAL QUERIES ============

def check_hospital_capacity(hospital_id: str) -> dict:
    """Check capacity and services of a specific hospital (placeholder)."""
    # Placeholder implementation
    return {"status": "placeholder", "message": "Hospital capacity check not yet implemented"}


# ============ SUPPLY QUERIES ============

def check_supply_inventory(supply_id: str) -> dict:
    """Check inventory for a specific supply resource (placeholder)."""
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

You have access to tools for:
- Getting available shelter information by location with optional filters
- Getting ongoing storm information by location
- Checking hospital capacity (placeholder)
- Checking supply inventory (placeholder)

Use these tools to retrieve data from BigQuery. Return clear, structured results.""",
        tools=[
            get_available_shelter_info,
            get_ongoing_storms_info,
            check_hospital_capacity,
            check_supply_inventory,
        ],
    )
    logger.info("[create_big_query_data_agent] BigQuery Data agent created successfully")
    return big_query_agent

