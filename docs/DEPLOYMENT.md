# 🚀 Deployment Guide - First Responder Agent

Choose your deployment strategy based on your needs.

## Quick Start

**For Hackathons/Demos:**
```bash
./deploy-cloudrun.sh
```
See [DEPLOYMENT_CLOUDRUN.md](./DEPLOYMENT_CLOUDRUN.md) for details.

**For Production:**
```bash
./deploy-vertex-ai.sh
```
See [DEPLOYMENT_VERTEX_AI.md](./DEPLOYMENT_VERTEX_AI.md) for details.

---

## Deployment Options

### Option A: Everything on Cloud Run ⭐ Recommended for Hackathons

**One command deploys everything**

```bash
./deploy-cloudrun.sh
```

**Best for:**
- Hackathons and demos
- MVPs and prototypes
- Cost-sensitive projects
- Quick iterations

**Features:**
- ✅ Single deployment command
- ✅ All components in one container
- ✅ Simpler architecture and debugging
- ✅ Lower cost (no Vertex AI charges)
- ✅ Scales to zero when idle

📖 **[Full Guide: DEPLOYMENT_CLOUDRUN.md](./DEPLOYMENT_CLOUDRUN.md)**

---

### Option B: Vertex AI Agent Engine + Cloud Run UI

**Production-ready architecture with independent scaling**

```bash
./deploy-vertex-ai.sh
```

**Best for:**
- Production deployments
- Enterprise applications
- Independent agent updates
- Advanced monitoring needs

**Features:**
- ✅ Agent runs on Google's managed infrastructure
- ✅ Independent scaling (agent vs UI)
- ✅ Update agent without redeploying UI
- ✅ Enterprise-grade monitoring
- ✅ Better for high-scale workloads

📖 **[Full Guide: DEPLOYMENT_VERTEX_AI.md](./DEPLOYMENT_VERTEX_AI.md)**

---

## Architecture Comparison

### Option A: Everything on Cloud Run

```
┌─────────────────────────────────────────────────────────────┐
│                     Google Cloud Platform                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Cloud Run Container (Port 8080)            │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Nginx Reverse Proxy                           │  │   │
│  │  │  - Routes / → Next.js UI (port 3000)           │  │   │
│  │  │  - Routes /api/agent → FastAPI (port 8000)     │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────┐        ┌──────────────────────┐    │   │
│  │  │  Next.js UI  │        │  FastAPI Backend     │    │   │
│  │  │  (Port 3000) │◄──────►│  (Port 8000)         │    │   │
│  │  │              │        │  + AG-UI ADK         │    │   │
│  │  │  CopilotKit  │        │  + Agent Logic       │    │   │
│  │  └──────────────┘        └──────────────────────┘    │   │
│  │                                    │                 │   │
│  │                          ┌─────────┴─────────┐       │   │
│  │                          │ Multi-Agent System│       │   │
│  │                          │ - Disaster Agent  │       │   │
│  │                          │ - Relief Agent    │       │   │
│  │                          │ - Insights Agent  │       │   │
│  │                          └─────────┬─────────┘       │   │
│  └────────────────────────────────────┼─────────────────┘   │
│                                       │                     │
│                                       ▼                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │     External APIs                                  │     │
│  │     - BigQuery (storm/shelter data)                │     │
│  │     - FEMA API (disaster declarations)             │     │
│  │     - NOAA API (weather alerts)                    │     │
│  │     - Google Maps API (geocoding/places)           │     │
│  └────────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Option B: Vertex AI Agent Engine + Cloud Run UI

```
┌─────────────────────────────────────────────────────────────┐
│                     Google Cloud Platform                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Cloud Run Container (Port 8080)            │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Nginx Reverse Proxy                           │  │   │
│  │  │  - Routes / → Next.js UI (port 3000)           │  │   │
│  │  │  - Routes /api/agent → FastAPI (port 8000)     │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────┐        ┌──────────────────────┐    │   │
│  │  │  Next.js UI  │        │  FastAPI Backend     │    │   │
│  │  │  (Port 3000) │◄──────►│  (Port 8000)         │    │   │
│  │  │              │        │  + AG-UI ADK         │    │   │
│  │  │  CopilotKit  │        │  (API Wrapper)       │    │   │
│  │  └──────────────┘        └──────────┬───────────┘    │   │
│  └─────────────────────────────────────┼────────────────┘   │
│                                        │                    │
│                                        │ API Calls          │
│                                        ▼                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │     Vertex AI Agent Engine (Managed Service)       │     │
│  │  ┌──────────────────────────────────────────────┐  │     │
│  │  │         Multi-Agent System                   │  │     │
│  │  │         - Disaster Discovery Agent           │  │     │
│  │  │         - Relief Finder Agent                │  │     │
│  │  │         - Insights Agent                     │  │     │
│  │  └──────────────────┬───────────────────────────┘  │     │
│  └─────────────────────┼──────────────────────────────┘     │
│                        │                                    │
│                        ▼                                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │     External APIs                                  │     │
│  │     - BigQuery (storm/shelter data)                │     │
│  │     - FEMA API (disaster declarations)             │     │
│  │     - NOAA API (weather alerts)                    │     │
│  │     - Google Maps API (geocoding/places)           │     │
│  └────────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Matrix

| Use Case | Recommended Option | Deployment Script |
|----------|-------------------|-------------------|
| **Hackathon/Demo** | Option A | `./deploy-cloudrun.sh` |
| **MVP/Prototype** | Option A | `./deploy-cloudrun.sh` |
| **Production (small scale)** | Option A | `./deploy-cloudrun.sh` |
| **Production (enterprise)** | Option B | `./deploy-vertex-ai.sh` |
| **Need independent agent updates** | Option B | `./deploy-vertex-ai.sh` |
| **Cost-sensitive** | Option A | `./deploy-cloudrun.sh` |
| **Need advanced monitoring** | Option B | `./deploy-vertex-ai.sh` |

---

## Detailed Guides

- 📖 **[Option A: Cloud Run Only](./DEPLOYMENT_CLOUDRUN.md)** - Complete guide for single-container deployment
- 📖 **[Option B: Vertex AI + Cloud Run](./DEPLOYMENT_VERTEX_AI.md)** - Complete guide for production architecture

---

## Quick Reference

### Environment Variables

**Option A (Cloud Run only):**
```bash
GCP_PROJECT=your-project-id
GCP_REGION=us-central1
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-maps-api-key
```

**Option B (Vertex AI + Cloud Run):**
```bash
GCP_PROJECT=your-project-id
GCP_REGION=us-central1
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-maps-api-key
STAGING_BUCKET=gs://your-staging-bucket
RESOURCE_NAME=projects/.../locations/.../reasoningEngines/...
```

### Deployment Commands

**Option A:**
```bash
./deploy-cloudrun.sh
```

**Option B:**
```bash
./deploy-vertex-ai.sh
```

### Monitoring

**Option A:**
```bash
gcloud run logs tail first-responder-agent --region us-central1
```

**Option B:**
```bash
# UI logs
gcloud run logs tail first-responder-agent-ui --region us-central1

# Agent logs
# View in Cloud Console: https://console.cloud.google.com/logs
```

---

## Support

For detailed instructions, troubleshooting, and advanced configuration:
- See [DEPLOYMENT_CLOUDRUN.md](./DEPLOYMENT_CLOUDRUN.md) for Option A
- See [DEPLOYMENT_VERTEX_AI.md](./DEPLOYMENT_VERTEX_AI.md) for Option B

