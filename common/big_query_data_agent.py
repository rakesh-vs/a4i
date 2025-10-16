"""Common BigQuery Data Agent - Shared across multiple agents for various use cases."""

import os
import logging
from google.cloud import bigquery
from google.adk.agents import Agent

from typing import Optional

logger = logging.getLogger(__name__)


def _get_bigquery_client():
    """Get BigQuery client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return bigquery.Client(project=project_id)


# ============ DISASTER/STORM QUERIES ============

def query_storms_by_state(state: str, limit: int = 10) -> dict:
    """Query storm events by state from NOAA database."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id, state, event_type, begin_date_time, end_date_time,
            injuries_direct, injuries_indirect, deaths_direct, deaths_indirect,
            damage_property, damage_crops
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE state = '{state.upper()}'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "state": state.upper(), "count": len(rows), "storms": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query storms for {state}: {str(e)}"}


def query_storms_by_date_range(start_date: str, end_date: str, limit: int = 20) -> dict:
    """Query storm events within a date range."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id, state, event_type, begin_date_time, end_date_time,
            injuries_direct, deaths_direct, damage_property
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE DATE(begin_date_time) >= '{start_date}'
          AND DATE(begin_date_time) <= '{end_date}'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "date_range": f"{start_date} to {end_date}", "count": len(rows), "storms": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query storms for date range: {str(e)}"}


def query_storms_by_type(event_type: str, limit: int = 15) -> dict:
    """Query storm events by type."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id, state, event_type, begin_date_time,
            injuries_direct, deaths_direct, damage_property
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE event_type LIKE '%{event_type}%'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "event_type": event_type, "count": len(rows), "storms": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query storms by type: {str(e)}"}


def query_storm_statistics(state: Optional[str] = None) -> dict:
    """Get aggregated storm statistics."""
    try:
        client = _get_bigquery_client()
        where_clause = f"WHERE state = '{state.upper()}'" if state else ""
        query = f"""
        SELECT 
            state, COUNT(*) as total_events,
            SUM(injuries_direct) as total_injuries,
            SUM(deaths_direct) as total_deaths,
            SUM(CAST(damage_property AS FLOAT64)) as total_property_damage
        FROM `bigquery-public-data.noaa_gsod.storms`
        {where_clause}
        GROUP BY state
        ORDER BY total_events DESC
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "statistics": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to get storm statistics: {str(e)}"}


# ============ SHELTER QUERIES ============

def query_shelters_by_city(city_name: str, limit: int = 10) -> dict:
    """Query available shelters in a city.
    
    Args:
        city_name: Name of the city
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with status and results
    """
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT * FROM qwiklabs-gcp-00-fb4bb5fddc00.c4datasetnew.Shelter 
        where CITY = '{city_name}'
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "city": city_name, "count": len(rows), "shelters": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query shelters: {str(e)}"}


def check_shelter_capacity(shelter_id: str) -> dict:
    """Check capacity and availability of a specific shelter."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            shelter_id, name, capacity, current_occupancy,
            (capacity - current_occupancy) as available_beds
        FROM `bigquery-public-data.disaster_relief.shelters`
        WHERE shelter_id = '{shelter_id}'
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        if rows:
            return {"status": "success", "shelter_id": shelter_id, "capacity_info": rows[0]}
        else:
            return {"status": "not_found", "shelter_id": shelter_id}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to check shelter capacity: {str(e)}"}


# ============ HOSPITAL QUERIES ============

def query_hospitals_by_location(location: str, limit: int = 10) -> dict:
    """Query available hospitals in a location."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            hospital_id, name, location, bed_capacity, available_beds,
            address, phone, specialties
        FROM `bigquery-public-data.disaster_relief.hospitals`
        WHERE location LIKE '%{location}%'
        ORDER BY available_beds DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "location": location, "count": len(rows), "hospitals": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query hospitals: {str(e)}"}


def check_hospital_capacity(hospital_id: str) -> dict:
    """Check capacity and services of a specific hospital."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            hospital_id, name, bed_capacity, available_beds,
            emergency_dept, icu_beds, trauma_center
        FROM `bigquery-public-data.disaster_relief.hospitals`
        WHERE hospital_id = '{hospital_id}'
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        if rows:
            return {"status": "success", "hospital_id": hospital_id, "capacity_info": rows[0]}
        else:
            return {"status": "not_found", "hospital_id": hospital_id}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to check hospital capacity: {str(e)}"}


# ============ SUPPLY QUERIES ============

def query_supplies_by_location(supply_type: str, location: str, limit: int = 10) -> dict:
    """Query available relief supplies in a location."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            supply_id, supply_type, quantity, location, warehouse,
            address, phone, last_updated
        FROM `bigquery-public-data.disaster_relief.supplies`
        WHERE supply_type LIKE '%{supply_type}%'
          AND location LIKE '%{location}%'
        ORDER BY quantity DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {"status": "success", "supply_type": supply_type, "location": location, "count": len(rows), "supplies": rows}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to query supplies: {str(e)}"}


def check_supply_inventory(supply_id: str) -> dict:
    """Check inventory for a specific supply resource."""
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            supply_id, supply_type, quantity, unit, warehouse, location
        FROM `bigquery-public-data.disaster_relief.supplies`
        WHERE supply_id = '{supply_id}'
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        if rows:
            return {"status": "success", "supply_id": supply_id, "inventory_info": rows[0]}
        else:
            return {"status": "not_found", "supply_id": supply_id}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to check supply inventory: {str(e)}"}


def create_big_query_data_agent():
    """Create and return the common BigQuery Data agent."""
    logger.info("[create_big_query_data_agent] Creating common BigQuery Data agent")
    
    big_query_agent = Agent(
        name="big_query_data_agent",
        model="gemini-2.5-flash",
        description="Common agent for querying BigQuery data for disasters, shelters, hospitals, and supplies",
        instruction="""You are a common BigQuery Data Agent used by multiple agents for querying disaster and relief data.

You have access to tools for:
- Querying storm events by state, date range, or type
- Getting storm statistics
- Querying shelters and checking capacity
- Querying hospitals and checking capacity
- Querying supplies and checking inventory

Use these tools to retrieve data from BigQuery. Return clear, structured results.""",
        tools=[
            query_storms_by_state,
            query_storms_by_date_range,
            query_storms_by_type,
            query_storm_statistics,
            query_shelters_by_city,
            check_shelter_capacity,
            query_hospitals_by_location,
            check_hospital_capacity,
            query_supplies_by_location,
            check_supply_inventory,
        ],
    )
    logger.info("[create_big_query_data_agent] BigQuery Data agent created successfully")
    return big_query_agent

