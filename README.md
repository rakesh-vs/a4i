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
2. Click the chat sidebar on the right
3. Ask questions like:
   - "What disasters are happening near San Francisco?"
   - "Find relief resources in Los Angeles"
   - "What's the weather situation in Miami?"

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

### Backend
- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **API**: FastAPI + Uvicorn
- **Data Sources**:
  - BigQuery (historical storm and shelter data)
  - FEMA OpenFEMA API (disaster declarations)
  - NOAA Weather API (weather alerts and forecasts)
  - Google Maps API (geocoding and mapping)
- **Language**: Python 3.12+
- **Dependencies**:
  - `google-adk>=1.16.0` - Agent framework
  - `fastapi>=0.104.0` - Web API framework
  - `uvicorn>=0.24.0` - ASGI server
  - `ag-ui-adk>=0.3.1` - AG-UI protocol adapter for ADK
  - `pydantic>=2.12.2` - Data validation
  - `python-dotenv>=1.1.1` - Environment configuration

### Frontend
- **Framework**: Next.js 15+ (React)
- **UI Library**: CopilotKit React Components
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Dependencies**:
  - `@copilotkit/react-core` - CopilotKit core
  - `@copilotkit/react-ui` - CopilotKit UI components
  - `@copilotkit/runtime` - CopilotKit runtime
  - `@ag-ui/client` - AG-UI client for ADK integration

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
├── first_responder_agent/                # Core agent system
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
├── agent/                                # FastAPI backend wrapper
│   ├── main.py                           # FastAPI app with AG-UI ADK integration
│   └── __init__.py
├── ui/                                   # Next.js frontend
│   ├── app/
│   │   ├── api/copilotkit/
│   │   │   └── route.ts                  # CopilotKit API route with HttpAgent
│   │   ├── layout.tsx                    # Root layout with CopilotKit provider
│   │   ├── page.tsx                      # Main page with chat interface
│   │   └── globals.css                   # Global styles
│   ├── package.json                      # Node.js dependencies
│   └── next.config.ts                    # Next.js configuration
├── deploy.py                             # Cloud deployment script
├── runner.py                             # CLI conversational runner
├── pyproject.toml                        # Python project configuration
├── .env                                  # Environment variables (not in git)
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

