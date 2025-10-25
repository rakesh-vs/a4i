# First Responder Agent (a4i)

An intelligent multi-agent system for emergency response coordination and disaster management. The system orchestrates multiple specialized AI agents to discover disasters, locate relief resources, and synthesize actionable intelligence for first responders.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Workflow Execution](#-workflow-execution)
- [Package Management](#-package-management)
- [Deployment](#-deployment)
- [Runner](#-conversational-runner)
- [Environment Configuration](#-environment-configuration)
- [Core Components](#-core-components)
- [Tech Stack](#-tech-stack)
- [Key Features](#-key-features)
- [Project Structure](#-project-structure)
- [Agent Communication](#-agent-communication)
- [Extensibility](#-extensibility)

## 🏗️ Architecture Overview

The First Responder Agent follows a **hierarchical multi-agent architecture** with a root coordinator agent and specialized sub-agents for different domains:

```
┌─────────────────────────────────────────────────────────────────┐
│                  First Responder Root Agent                      │
│              (Orchestrates workflow & coordinates)               │
└────────────────┬──────────────────────┬──────────────────────────┘
                 │                      │
        ┌────────▼────────┐    ┌────────▼────────┐    ┌────────────────┐
        │  Disaster       │    │  Relief         │    │  Insights      │
        │  Discovery      │    │  Finder         │    │  Agent         │
        │  Agent          │    │  Agent          │    │                │
        └────────┬────────┘    └────────┬────────┘    └────────────────┘
                 │                      │
        ┌────────┴──────────┬───────┐   │
        │                   │       │   │
    ┌───▼──┐  ┌────▼────┐ ┌─▼──┐  ┌──▼──────┐  ┌──────────┐  ┌──────────┐
    │BigQ  │  │FEMA     │ │NOAA│  │Shelter  │  │Hospital  │  │Supply    │
    │Data  │  │Live     │ │Live│  │Finder   │  │Finder    │  │Finder    │
    │Agent │  │Agent    │ │Ag │  │Agent    │  │Agent     │  │Agent     │
    └──────┘  └─────────┘ └────┘  └─────────┘  └──────────┘  └──────────┘
```

## 🔄 Workflow Execution

The system executes a coordinated workflow automatically:

1. **Location Input** - User provides their location (or is prompted for it)
2. **Geocoding** - Location string is converted to latitude/longitude coordinates
3. **Disaster Discovery** - Parallel queries to:
   - BigQuery for historical storm data
   - FEMA Live API for disaster declarations
   - NOAA Live API for weather alerts
4. **Relief Resource Discovery** - Parallel queries to locate:
   - Shelters and emergency housing
   - Hospitals and medical facilities
   - Relief supplies and resources
5. **Insights Synthesis** - Comprehensive analysis combining all data into actionable recommendations

## 📦 Package Management

This project uses **UV** for fast Python package management.

```bash
# Install dependencies
uv sync

# Add a dependency
uv add package_name

# Add a dev dependency
uv add --dev package_name

# Update dependencies
uv sync --upgrade
```

The `uv.lock` file ensures reproducible builds across environments.

## 🚀 Deployment

The system is deployed to Google Cloud using the ADK deployment tool:

```bash
python deploy.py
```

## 💬 Conversational Runner

After deployment, interact with the agent through a conversational chat interface:

```bash
uv run python runner.py
```

This starts an interactive chat loop where you can:
- Type messages to query the First Responder Agent
- Receive streaming responses in real-time
- Have multi-turn conversations
- Exit with `exit` or `quit` commands

The runner uses environment variables from `.env` to connect to your deployed agent.

## 🔑 Environment Configuration

For required environment variables, refer `.env.example`

## 📦 Core Components

### Root Agent: `first_responder_agent/agent.py`
- **Name**: `first_responder`
- **Model**: Gemini 2.5 Flash
- **Role**: Main orchestrator that coordinates the workflow
- **Tools**: Geocoding utility
- **Sub-agents**: Disaster Discovery, Relief Finder, Insights

### Disaster Discovery Agent: `disaster_discovery_agent/agent.py`
Discovers and locates disasters using multiple data sources:

- **BigQuery Data Agent** (`common/big_query_data_agent.py`)
  - Queries historical storm locations and data
  - Proximity-based search (default 25-mile radius)
  - Queries shelter availability

- **FEMA Live Agent** (`disaster_discovery_agent/fema_live_agent/agent.py`)
  - Queries active disaster declarations
  - Retrieves FEMA assistance programs
  - Filters by state and disaster type

- **NOAA Live Agent** (`disaster_discovery_agent/noaa_live_agent/agent.py`)
  - Queries active weather alerts
  - Retrieves severe weather outlooks
  - Location-based weather queries

### Relief Finder Agent: `relief_finder_agent/agent.py`
Locates relief resources and support infrastructure:

- **Shelter Finder Agent** (`relief_finder_agent/shelter_finder_agent.py`)
  - Locates emergency shelters
  - Filters by capacity, services, and accessibility

- **Hospital Finder Agent** (`relief_finder_agent/hospital_finder_agent.py`)
  - Locates medical facilities
  - Queries hospital capacity and services

- **Supply Finder Agent** (`relief_finder_agent/supply_finder_agent.py`)
  - Locates relief supply distribution points
  - Checks inventory availability

### Insights Agent: `insights_agent/agent.py`
Synthesizes all collected data into comprehensive analysis:
- Combines disaster and relief data
- Generates actionable recommendations
- Prioritizes response actions
- Provides situational awareness

### Common Utilities: `common/`

- **Geocoding** (`common/geocoding.py`)
  - Converts location strings to coordinates
  - Uses Google Maps Geocoding API

- **Google Maps MCP Agent** (`common/google_maps_mcp_agent.py`)
  - Provides map visualization
  - Calculates distances and routes
  - Uses Model Context Protocol (MCP)

## 🔧 Tech Stack

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **Data Sources**:
  - BigQuery (historical storm and shelter data)
  - FEMA OpenFEMA API (disaster declarations)
  - NOAA Weather API (weather alerts and forecasts)
  - Google Maps API (geocoding and mapping)
- **Language**: Python 3.11+
- **Dependencies**:
  - `google-adk>=1.16.0` - Agent framework
  - `pydantic>=2.12.2` - Data validation
  - `python-dotenv>=1.1.1` - Environment configuration

## 🎯 Key Features

- **Automatic Workflow Execution** - No manual intervention between steps
- **Parallel Data Collection** - Multiple agents query simultaneously
- **Multi-Source Integration** - Combines historical, real-time, and predictive data
- **Intelligent Synthesis** - AI-powered analysis of complex disaster scenarios
- **Scalable Architecture** - Easy to add new agents and data sources
- **Comprehensive Logging** - Detailed execution tracking for debugging

## 📝 Project Structure

```
a4i/
├── first_responder_agent/
│   ├── agent.py                          # Root agent
│   ├── common/
│   │   ├── geocoding.py                  # Location geocoding
│   │   ├── big_query_data_agent.py       # BigQuery queries
│   │   └── google_maps_mcp_agent.py      # Map functionality
│   ├── disaster_discovery_agent/
│   │   ├── agent.py                      # Disaster discovery coordinator
│   │   ├── fema_live_agent/
│   │   │   └── agent.py                  # FEMA data queries
│   │   └── noaa_live_agent/
│   │       └── agent.py                  # NOAA data queries
│   ├── relief_finder_agent/
│   │   ├── agent.py                      # Relief finder coordinator
│   │   ├── shelter_finder_agent.py       # Shelter location queries
│   │   ├── hospital_finder_agent.py      # Hospital location queries
│   │   └── supply_finder_agent.py        # Supply location queries
│   └── insights_agent/
│       └── agent.py                      # Analysis & synthesis
├── deploy.py                             # Deployment script
├── pyproject.toml                        # Project configuration
└── README.md                             # This file
```

## 🔄 Agent Communication

Agents communicate through:
- **Tool Calls** - Agents invoke tools to query data
- **Sub-agent Delegation** - Parent agents delegate to child agents
- **Control Transfer** - Agents transfer control back to parent using `transfer_to_agent` tool
- **Structured Results** - All results returned as dictionaries with status and data

## 📈 Extensibility

The architecture supports easy extension:
- Add new data sources by creating new agents with appropriate tools
- Add new relief resource types by creating new finder agents
- Enhance analysis by extending the Insights Agent
- Integrate additional APIs through the MCP framework

