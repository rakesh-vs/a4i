# 🚀 Deployment Guide - Vertex AI + Cloud Run

**Option B: Vertex AI Agent Engine + Cloud Run UI** - Production-Ready Architecture

Deploy your First Responder Agent system with the agent backend on Vertex AI and the UI on Cloud Run for independent scaling and enterprise features.

## Architecture Overview

**Agent runs on Vertex AI, UI on Cloud Run:**

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

## Why Choose This Option?

**Pros:**
- ✅ **Agent runs on Google's managed infrastructure** - No container management
- ✅ **Independent scaling** - Agent and UI scale separately
- ✅ **Update agent without redeploying UI** - Faster iterations
- ✅ **Enterprise-grade monitoring** - Advanced Vertex AI features
- ✅ **Better for production workloads** - Proven at scale

**Cons:**
- ⚠️ More complex deployment (2 stages)
- ⚠️ Higher cost (Vertex AI + Cloud Run)
- ⚠️ More moving parts to debug

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **APIs Enabled**:
   - Cloud Run API
   - Container Registry API
   - Vertex AI API
   - BigQuery API
   - Cloud Storage API
3. **gcloud CLI** installed and authenticated
4. **Docker** installed locally
5. **Environment Variables** configured in `.env` file

## Step 1: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
GCP_PROJECT=your-project-id
GCP_REGION=us-central1

# API Keys
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-maps-api-key

# Deployment Configuration
STAGING_BUCKET=gs://your-staging-bucket

# Agent Engine Configuration (will be populated after Stage 1)
# RESOURCE_NAME=projects/.../locations/.../reasoningEngines/...
```

## Step 2: Deploy Using Automated Script

We provide an automated script that handles both stages:

```bash
# Make the deployment script executable (already done)
chmod +x deploy-vertex-ai.sh

# Run the deployment
./deploy-vertex-ai.sh
```

The script will:

### Stage 1: Deploy Agent to Vertex AI
1. ✅ Run `python deploy.py`
2. ✅ Deploy your multi-agent system to Vertex AI Agent Engine
3. ⏸️ Prompt you to copy `RESOURCE_NAME` to `.env`

### Stage 2: Deploy UI to Cloud Run
4. ✅ Create optimized Dockerfile (UI only, no agent logic)
5. ✅ Build Docker image
6. ✅ Push to Google Container Registry
7. ✅ Deploy to Cloud Run with Vertex AI connection
8. ✅ Output the public URL

## Manual Deployment (Alternative)

If you prefer manual control:

### Stage 1: Deploy Agent Backend

```bash
# Deploy agent to Vertex AI
python deploy.py
```

**Important:** Copy the `RESOURCE_NAME` from the output:
```
AgentEngine created. Resource name: projects/803199707059/locations/us-central1/reasoningEngines/8485261085035724800
```

Add it to your `.env` file:
```bash
RESOURCE_NAME=projects/803199707059/locations/us-central1/reasoningEngines/8485261085035724800
```

### Stage 2: Deploy UI to Cloud Run

```bash
# Build and deploy UI
docker build -f Dockerfile.vertex-ai -t gcr.io/${GCP_PROJECT}/first-responder-agent-ui:latest .
docker push gcr.io/${GCP_PROJECT}/first-responder-agent-ui:latest

gcloud run deploy first-responder-agent-ui \
  --image gcr.io/${GCP_PROJECT}/first-responder-agent-ui:latest \
  --platform managed \
  --region ${GCP_REGION} \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY},RESOURCE_NAME=${RESOURCE_NAME},..."
```

## Step 3: Verify Deployment

Once deployed, you'll receive a URL like:
```
https://first-responder-agent-ui-xxxxx-uc.a.run.app
```

### Test the Deployment

1. **Open the URL** in your browser
2. **Wait for cold start** (first request may take 30-60 seconds)
3. **Test the chat interface** - Try asking: "What disasters are happening in Florida?"
4. **Check the map** - Verify markers appear for locations

### Monitor Logs

**Cloud Run Logs (UI):**
```bash
gcloud run logs tail first-responder-agent-ui --region us-central1
```

**Vertex AI Logs (Agent):**
```bash
# View in Cloud Console
https://console.cloud.google.com/logs
```

## Troubleshooting

### Agent Not Responding

1. Verify agent is deployed:
```bash
gcloud ai reasoning-engines list --region us-central1
```

2. Check if `RESOURCE_NAME` in Cloud Run matches the deployed agent
3. Verify API keys are valid
4. Check Vertex AI logs for errors

### UI Not Loading

1. Check Cloud Run logs
2. Verify Next.js build succeeded
3. Check browser console for errors

### Connection Issues Between UI and Agent

1. Verify `RESOURCE_NAME` environment variable is set correctly in Cloud Run
2. Check if Vertex AI API is enabled
3. Verify service account permissions

## Updating the Deployment

### Update Agent Only

```bash
# Redeploy agent to Vertex AI
python deploy.py

# Update RESOURCE_NAME in Cloud Run if it changed
gcloud run services update first-responder-agent-ui \
  --update-env-vars RESOURCE_NAME=new-resource-name \
  --region us-central1
```

### Update UI Only

```bash
# Rebuild and redeploy UI
./deploy-vertex-ai.sh
# (Skip Stage 1 when prompted)
```

## Cost Optimization

### Vertex AI Pricing
- **Agent queries** - Pay per query
- **Storage** - Minimal for agent artifacts

### Cloud Run Pricing
- **CPU/Memory usage** - Only when handling requests
- **Request count** - $0.40 per million requests

Tips to reduce costs:
1. Set Cloud Run `--min-instances=0` to scale to zero
2. Monitor Vertex AI query costs
3. Implement caching for frequent queries
4. Use appropriate timeout values

## Security Considerations

### Production Deployment Checklist

- [ ] Enable authentication on Cloud Run
- [ ] Restrict Vertex AI access with IAM
- [ ] Use Secret Manager for API keys
- [ ] Enable VPC Service Controls
- [ ] Set up Cloud Armor for DDoS protection
- [ ] Configure custom domain with SSL
- [ ] Enable audit logging
- [ ] Set up monitoring and alerting

### Enable Authentication

**Cloud Run:**
```bash
gcloud run deploy first-responder-agent-ui \
  --no-allow-unauthenticated \
  --region us-central1
```

**Vertex AI:**
Use IAM roles to control access to the agent engine.

## Advanced Configuration

### Custom Domain

```bash
gcloud run domain-mappings create \
  --service first-responder-agent-ui \
  --domain your-domain.com \
  --region us-central1
```

### Scaling Configuration

**Cloud Run:**
```bash
gcloud run services update first-responder-agent-ui \
  --min-instances=1 \
  --max-instances=50 \
  --concurrency=80 \
  --region us-central1
```

**Vertex AI:**
Scaling is handled automatically by Google.

## Next Steps

After successful deployment:
1. Set up monitoring and alerting for both services
2. Configure custom domain
3. Enable authentication for production
4. Set up CI/CD pipeline for automated deployments
5. Implement rate limiting
6. Add caching layer for frequently accessed data
7. Monitor costs and optimize resource usage

## Need Simpler Deployment?

If you don't need independent scaling or enterprise features, consider [Option A: Cloud Run Only](./DEPLOYMENT_CLOUDRUN.md) for a simpler, more cost-effective solution.

