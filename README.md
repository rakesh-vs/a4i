# First Responder Agent (a4i)

An intelligent multi-agent system for emergency response coordination and disaster management. The system orchestrates multiple specialized AI agents to discover disasters, locate relief resources, and synthesize actionable intelligence for first responders.

**NEW**: Now with a modern web UI powered by CopilotKit + Next.js!

## 📋 Table of Contents

- [Quick Start - Web UI](#-quick-start---web-ui)
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

## 🚀 Quick Start - Web UI

### Prerequisites
- Python 3.12+
- Node.js 18+
- Google Cloud credentials (for agent functionality)

### Setup

1. **Clone and install Python dependencies**:
```bash
# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
uv pip install -e .
```

2. **Install Node.js dependencies**:
```bash
cd ui
npm install
cd ..
```

3. **Configure environment variables**:
```bash
# Copy .env.example to .env and fill in your credentials
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

4. **Run the development servers**:

**Terminal 1 - Agent Backend:**
```bash
source .venv/bin/activate
cd agent
python main.py
```

**Terminal 2 - Next.js UI:**
```bash
cd ui
npm run dev
```

5. **Open the app**:
- Web UI: http://localhost:3000
- Agent API: http://localhost:8000

### Usage

1. Open http://localhost:3000 in your browser
2. The UI features a 3-column layout:
   - **Left**: Interactive map showing disaster locations and relief resources
   - **Center**: Chat interface for conversing with the agent
   - **Right**: Agent activity panel showing real-time workflow progress
3. Ask questions like:
   - "What disasters are happening near San Francisco?"
   - "Find relief resources in Los Angeles"
   - "What's the weather situation in Miami?"
4. Watch the map update with markers and the activity panel track agent execution

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

1. **Location Input** - User provides their location via chat interface
2. **Geocoding** - Root agent uses `geocode_location` tool to convert location string to coordinates
3. **Disaster Discovery** - Root agent delegates to disaster_discovery_agent which:
   - Queries BigQuery for historical storm data using `get_ongoing_storms_info` tool
   - Delegates to fema_live_agent for active disaster declarations
   - Delegates to noaa_live_agent for weather alerts
4. **Relief Resource Discovery** - Root agent delegates to relief_finder_agent which:
   - Calls `find_shelters` tool (combines BigQuery + Google Maps)
   - Calls `find_hospitals` tool (combines BigQuery + Google Maps)
   - Calls `find_supplies` tool (uses Google Maps)
5. **Insights Synthesis** - Root agent delegates to insights_agent for comprehensive analysis
6. **Map Updates** - Throughout execution, tools automatically update the shared state with location markers
7. **Final Response** - Root agent presents synthesized insights to user via chat

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
- **Tools**: `geocode_location` (converts location strings to coordinates)
- **Sub-agents**: Disaster Discovery, Relief Finder, Insights
- **State Management**: Tracks locations, map center, current agent, and activity history

### Disaster Discovery Agent: `disaster_discovery_agent/agent.py`
Discovers and locates disasters using multiple data sources:

- **BigQuery Storm Data Tool** (`common/bigquery_tools.py`)
  - Queries historical storm locations and data from BigQuery
  - Proximity-based search (default 25-mile radius)
  - Accesses `StormLocations` dataset

- **FEMA Live Agent** (`disaster_discovery_agent/fema_live_agent/agent.py`)
  - Queries active disaster declarations via OpenFEMA API
  - Retrieves FEMA assistance programs and funding information
  - Filters by state and disaster type

- **NOAA Live Agent** (`disaster_discovery_agent/noaa_live_agent/agent.py`)
  - Queries active weather alerts via NOAA Weather API
  - Retrieves severe weather outlooks
  - Location-based weather queries

### Relief Finder Agent: `relief_finder_agent/agent.py`
Locates relief resources and support infrastructure:

- **Shelter Finder Tool** (`relief_finder_agent/shelter_finder_tool.py`)
  - Combines BigQuery shelter data with Google Maps Places API
  - Locates emergency shelters and lodging facilities
  - Provides comprehensive shelter information

- **Hospital Finder Tool** (`relief_finder_agent/hospital_finder_tool.py`)
  - Combines BigQuery hospital data with Google Maps Places API
  - Locates medical facilities
  - Queries hospital capacity and services

- **Supply Finder Tool** (`relief_finder_agent/supply_finder_tool.py`)
  - Uses Google Maps Places API to find pharmacies
  - Locates relief supply distribution points

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

- **BigQuery Tools** (`common/bigquery_tools.py`)
  - Queries storm data from BigQuery `StormLocations` dataset
  - Queries shelter data from BigQuery `Shelter` dataset
  - Provides hospital capacity checking (placeholder)
  - Provides supply inventory checking (placeholder)

- **Search Places Tool** (`common/search_places_tool.py`)
  - Searches for nearby places using Google Maps Places API
  - Automatically updates map state with location markers
  - Supports multiple place types (hospitals, shelters, pharmacies, etc.)

- **State Tools** (`common/state_tools.py`)
  - Manages agent activity tracking
  - Updates shared state across agents

## 🔧 Tech Stack

### Backend
- **Framework**: Google ADK (Agent Development Kit)
- **LLM Models**:
  - Gemini 2.5 Flash (root agent, sub-agents)
  - Gemini 2.5 Pro (disaster discovery agent)
- **API**: FastAPI + Uvicorn
- **Data Sources**:
  - BigQuery (historical storm data from `StormLocations`, shelter data from `Shelter`)
  - FEMA OpenFEMA API (disaster declarations and assistance programs)
  - NOAA Weather API (active weather alerts)
  - Google Maps API (geocoding and places search)
- **Language**: Python 3.12+
- **Package Manager**: UV (fast Python package manager)
- **Dependencies**:
  - `google-adk>=1.16.0` - Agent framework
  - `fastapi>=0.104.0` - Web API framework
  - `uvicorn>=0.24.0` - ASGI server
  - `ag-ui-adk>=0.3.1` - AG-UI protocol adapter for ADK
  - `pydantic>=2.12.2` - Data validation
  - `python-dotenv>=1.1.1` - Environment configuration
  - `googlemaps>=4.10.0` - Google Maps API client

### Frontend
- **Framework**: Next.js 16.0.0 (React 19.2.0)
- **UI Library**: CopilotKit React Components
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript 5
- **Map Libraries**: Leaflet + React Leaflet
- **Dependencies**:
  - `@copilotkit/react-core@^1.10.6` - CopilotKit core
  - `@copilotkit/react-ui@^1.10.6` - CopilotKit UI components
  - `@copilotkit/runtime@^1.10.6` - CopilotKit runtime
  - `@ag-ui/client@^0.0.40` - AG-UI client for ADK integration
  - `leaflet@^1.9.4` - Interactive maps
  - `react-leaflet@^5.0.0` - React wrapper for Leaflet

## 🎯 Key Features

- **Modern Web UI** - Interactive 3-column layout with map, chat, and agent activity tracking
- **Real-time Agent Monitoring** - Visual feedback on agent execution and workflow progress
- **Interactive Map** - Leaflet-based map showing disaster locations and relief resources
- **Automatic Workflow Execution** - No manual intervention between steps
- **Multi-Source Data Integration** - Combines BigQuery, FEMA, NOAA, and Google Maps data
- **Intelligent Synthesis** - AI-powered analysis of complex disaster scenarios
- **Scalable Architecture** - Easy to add new agents and data sources
- **Comprehensive Logging** - Detailed execution tracking for debugging
- **State Management** - Shared state across agents for coordinated responses

## 📝 Project Structure

```
a4i/
├── first_responder_agent/                # Core agent system
│   ├── agent.py                          # Root agent
│   ├── common/
│   │   ├── geocoding.py                  # Location geocoding
│   │   ├── bigquery_tools.py             # BigQuery queries (storms, shelters)
│   │   ├── search_places_tool.py         # Google Maps Places API integration
│   │   └── state_tools.py                # Agent state management
│   ├── disaster_discovery_agent/
│   │   ├── agent.py                      # Disaster discovery coordinator
│   │   ├── fema_live_agent/
│   │   │   └── agent.py                  # FEMA OpenFEMA API queries
│   │   └── noaa_live_agent/
│   │       └── agent.py                  # NOAA Weather API queries
│   ├── relief_finder_agent/
│   │   ├── agent.py                      # Relief finder coordinator
│   │   ├── shelter_finder_tool.py        # Shelter location tool
│   │   ├── hospital_finder_tool.py       # Hospital location tool
│   │   └── supply_finder_tool.py         # Supply location tool
│   └── insights_agent/
│       └── agent.py                      # Analysis & synthesis
├── agent/                                # FastAPI backend wrapper
│   ├── main.py                           # FastAPI app with AG-UI ADK integration
│   └── __init__.py
├── ui/                                   # Next.js frontend
│   ├── app/
│   │   ├── api/copilotkit/
│   │   │   └── route.ts                  # CopilotKit API route with AG-UI client
│   │   ├── layout.tsx                    # Root layout with CopilotKit provider
│   │   ├── page.tsx                      # Main page with 3-column layout
│   │   └── globals.css                   # Global styles
│   ├── components/
│   │   ├── MapPanel.tsx                  # Interactive map component
│   │   ├── AgentProcessingPanel.tsx      # Agent activity tracking panel
│   │   ├── LeafletMap.tsx                # Leaflet map implementation
│   │   └── ...                           # Other UI components
│   ├── package.json                      # Node.js dependencies
│   └── next.config.ts                    # Next.js configuration
├── deploy.py                             # Cloud deployment script (ADK)
├── runner.py                             # CLI conversational runner
├── pyproject.toml                        # Python project configuration
├── uv.lock                               # UV lock file for dependencies
├── .env.example                          # Example environment variables
└── README.md                             # This file
```

## 🔄 Agent Communication

Agents communicate through:
- **Tool Calls** - Agents invoke tools to query data (BigQuery, APIs, Google Maps)
- **Sub-agent Delegation** - Parent agents delegate to child agents for specialized tasks
- **Shared State** - All agents access and update shared state for coordination
- **Activity Tracking** - State tools track agent execution status (running, completed)
- **Structured Results** - All results returned as dictionaries with status and data
- **Callback Hooks** - `before_agent_callback` and `after_agent_callback` for state management

## 📈 Extensibility

The architecture supports easy extension:
- **Add New Data Sources** - Create new tools in `common/` or new sub-agents
- **Add Relief Resource Types** - Create new finder tools following the existing pattern
- **Enhance Analysis** - Extend the Insights Agent with additional analysis capabilities
- **Integrate New APIs** - Add new API integrations as tools or sub-agents
- **Customize UI** - Add new components to the Next.js frontend
- **Extend State** - Add new state fields for tracking additional information

