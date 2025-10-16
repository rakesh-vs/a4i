# Refactored Architecture

This document describes the refactored agent architecture following the plan in `plan.md`.

## Overview

The project has been rearchitected to use common shared modules that can be reused across multiple agents, reducing code duplication and improving maintainability. The system now includes an Insights Agent that synthesizes disaster and relief data into comprehensive analysis and actionable plans.

## Architecture Structure

```
first_responder_agent (root)
├── disaster_discovery_agent
│   ├── big_query_data_agent (common)
│   ├── fema_agent
│   └── noaa_agent
├── relief_finder_agent
│   ├── shelter_finder_agent
│   │   └── big_query_data_agent (common)
│   ├── hospital_finder_agent
│   │   └── big_query_data_agent (common)
│   └── supply_finder_agent
│       └── big_query_data_agent (common)
└── insights_agent (NEW)
    └── Synthesizes disaster and relief data into comprehensive analysis
```

## Common Shared Modules

### 1. `common/big_query_data_agent.py`
A unified BigQuery agent used across multiple agents for querying disaster and relief data.

**Capabilities:**
- **Disaster/Storm Queries:**
  - `query_storms_by_state()` - Query storms by state
  - `query_storms_by_date_range()` - Query storms within date range
  - `query_storms_by_type()` - Query storms by event type
  - `query_storm_statistics()` - Get aggregated storm statistics

- **Shelter Queries:**
  - `query_shelters_by_location()` - Find shelters in a location
  - `check_shelter_capacity()` - Check shelter capacity and availability

- **Hospital Queries:**
  - `query_hospitals_by_location()` - Find hospitals in a location
  - `check_hospital_capacity()` - Check hospital capacity and services

- **Supply Queries:**
  - `query_supplies_by_location()` - Find supplies in a location
  - `check_supply_inventory()` - Check supply inventory

### 2. `common/google_maps_mcp_agent.py`
A Google Maps MCP (Model Context Protocol) agent that provides all map functionality through the Google Maps API.

**Capabilities:**
- **Location Search:**
  - Find nearby places (shelters, hospitals, supplies, etc.)
  - Search for specific locations
  - Get location details and information

- **Map Operations:**
  - Display maps with custom markers and overlays
  - Calculate distances and routes between locations
  - Geocode addresses to coordinates and vice versa
  - Provide location-based information

**Note:** The old `common/map_tool.py` and `first_responder_agent/map_tool.py` are deprecated. All map functionality is now handled by the Google Maps MCP Agent.

## Agent Hierarchy

### First Responder Agent (Root)
- **Role:** Main emergency response coordination agent
- **Sub-agents:** disaster_discovery_agent, relief_finder_agent, insights_agent, google_maps_mcp_agent
- **Tools:** Google Maps MCP (location search, map display, geocoding, distance calculation)

### Disaster Discovery Agent
- **Role:** Discovers and locates disasters
- **Sub-agents:** big_query_data_agent, fema_agent, noaa_agent
- **Tools:** Location finder tools (find_disaster_location, geocode_address)

#### Big Query Data Agent (Common)
- **Role:** Queries historical disaster and relief data from BigQuery
- **Used by:** disaster_discovery_agent, shelter_finder_agent, hospital_finder_agent, supply_finder_agent

#### FEMA Agent
- **Role:** Queries live FEMA disaster data
- **Tools:** FEMA API queries

#### NOAA Agent (NEW)
- **Role:** Queries live NOAA weather alerts and data
- **Tools:** NOAA API queries

### Relief Finder Agent
- **Role:** Finds relief resources
- **Sub-agents:** shelter_finder_agent, hospital_finder_agent, supply_finder_agent

#### Shelter Finder Agent
- **Role:** Locates available shelters
- **Sub-agents:** big_query_data_agent (common)
- **Tools:** find_nearby_shelters, display_relief_resources_map

#### Hospital Finder Agent
- **Role:** Locates available hospitals
- **Sub-agents:** big_query_data_agent (common)
- **Tools:** find_nearby_hospitals, display_relief_resources_map

#### Supply Finder Agent
- **Role:** Locates available relief supplies
- **Sub-agents:** big_query_data_agent (common)
- **Tools:** find_nearby_supplies, display_relief_resources_map

### Insights Agent (NEW)
- **Role:** Synthesizes disaster and relief data into comprehensive analysis and actionable plans
- **Responsibilities:**
  - Analyzes disaster information and severity
  - Analyzes available relief resources
  - Creates detailed extraction and relief plans with phases
  - Identifies critical gaps and vulnerabilities
  - Provides key insights and recommendations
- **Output:** Comprehensive emergency brief with:
  - Disaster analysis and severity assessment
  - Critical insights and urgent areas
  - Phased extraction and relief plan (immediate, short-term, medium-term)
  - Resource deployment strategy
  - Key recommendations and next steps

## Key Improvements

1. **Code Reusability:** Common modules are shared across multiple agents, reducing duplication
2. **Scalability:** New agents can easily use the common big_query_data_agent and map_tool
3. **Maintainability:** Changes to common functionality only need to be made in one place
4. **Separation of Concerns:** Each agent has a clear, focused responsibility
5. **Live Data Integration:** Added NOAA agent for real-time weather alerts and data
6. **Comprehensive Relief Resources:** All relief finder agents now use the same data source and mapping tools

## File Structure

```
a4i/
├── common/
│   ├── __init__.py
│   ├── big_query_data_agent.py
│   ├── google_maps_mcp_agent.py
│   └── map_tool.py (deprecated - use google_maps_mcp_agent.py)
├── first_responder_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── map_tool.py (deprecated - use common/google_maps_mcp_agent.py)
├── disaster_discovery_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── location_finder.py
│   ├── bq_agent/ (deprecated - use common/big_query_data_agent.py)
│   ├── fema_agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   └── noaa_agent/
│       ├── __init__.py
│       └── agent.py
├── relief_finder_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── shelter_finder_agent.py
│   ├── hospital_finder_agent.py
│   └── supply_finder_agent.py
├── insights_agent/
│   ├── __init__.py
│   └── agent.py
└── plan.md
```

## Migration Notes

- The old `disaster_discovery_agent/bq_agent/` directory is now deprecated. Use `common/big_query_data_agent.py` instead.
- The old `first_responder_agent/map_tool.py` is now deprecated. Use `common/map_tool.py` instead.
- All relief finder sub-agents now use the common big_query_data_agent as a sub-agent.

