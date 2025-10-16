"""BigQuery agent for querying NOAA Storm Events Database."""

import os
from google.cloud import bigquery
from google.adk.agents import Agent


# Initialize BigQuery client
def _get_bigquery_client():
    """Get BigQuery client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return bigquery.Client(project=project_id)


def query_storms_by_state(state: str, limit: int = 10) -> dict:
    """Query storm events by state from NOAA database.
    
    Args:
        state: Two-letter state code (e.g., 'TX', 'CA')
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with status and results
    """
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id,
            state,
            event_type,
            begin_date_time,
            end_date_time,
            injuries_direct,
            injuries_indirect,
            deaths_direct,
            deaths_indirect,
            damage_property,
            damage_crops
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE state = '{state.upper()}'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {
            "status": "success",
            "state": state.upper(),
            "count": len(rows),
            "storms": rows
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query storms for {state}: {str(e)}"
        }


def query_storms_by_date_range(start_date: str, end_date: str, limit: int = 20) -> dict:
    """Query storm events within a date range.
    
    Args:
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        limit: Maximum number of results
        
    Returns:
        Dictionary with status and results
    """
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id,
            state,
            event_type,
            begin_date_time,
            end_date_time,
            injuries_direct,
            deaths_direct,
            damage_property
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE DATE(begin_date_time) >= '{start_date}'
          AND DATE(begin_date_time) <= '{end_date}'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {
            "status": "success",
            "date_range": f"{start_date} to {end_date}",
            "count": len(rows),
            "storms": rows
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query storms for date range: {str(e)}"
        }


def query_storms_by_type(event_type: str, limit: int = 15) -> dict:
    """Query storm events by type.
    
    Args:
        event_type: Type of storm event (e.g., 'Tornado', 'Hail', 'Flood')
        limit: Maximum number of results
        
    Returns:
        Dictionary with status and results
    """
    try:
        client = _get_bigquery_client()
        query = f"""
        SELECT 
            event_id,
            state,
            event_type,
            begin_date_time,
            injuries_direct,
            deaths_direct,
            damage_property
        FROM `bigquery-public-data.noaa_gsod.storms`
        WHERE event_type LIKE '%{event_type}%'
        ORDER BY begin_date_time DESC
        LIMIT {limit}
        """
        results = client.query(query).result()
        rows = [dict(row) for row in results]
        return {
            "status": "success",
            "event_type": event_type,
            "count": len(rows),
            "storms": rows
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to query storms by type: {str(e)}"
        }


def query_storm_statistics(state: str = None) -> dict:
    """Get aggregated storm statistics.
    
    Args:
        state: Optional state code for state-specific stats
        
    Returns:
        Dictionary with statistics
    """
    try:
        client = _get_bigquery_client()
        where_clause = f"WHERE state = '{state.upper()}'" if state else ""
        
        query = f"""
        SELECT 
            state,
            COUNT(*) as total_events,
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
        return {
            "status": "success",
            "statistics": rows
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get storm statistics: {str(e)}"
        }

def create_bigquery_agent():
    bigquery_agent = Agent(
        name="bigquery_agent",
        model="gemini-2.5-flash",
        description="Sub-agent for querying NOAA Storm Events from BigQuery",
        instruction="""You are a sub-agent that queries the NOAA Storm Events Database from BigQuery.
    You have access to tools to:
    - Query storms by state
    - Query storms by date range
    - Query storms by event type
    - Get storm statistics

    Use these tools to retrieve storm event data. Return clear, structured results.""",
        tools=[
            query_storms_by_state,
            query_storms_by_date_range,
            query_storms_by_type,
            query_storm_statistics,
        ],
    )

    return bigquery_agent

