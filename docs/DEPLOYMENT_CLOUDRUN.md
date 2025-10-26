# 🚀 Deployment Guide - Cloud Run Only

**Option A: Everything on Cloud Run** ⭐ Recommended for Hackathons

Deploy your complete First Responder Agent system (agent + backend + UI) in a single Cloud Run container.

## Architecture Overview

**Everything runs in a single Cloud Run container:**

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

## Why Choose This Option?

**Pros:**
- ✅ **Single deployment command** - Deploy everything with one script
- ✅ **All components in one container** - Simpler architecture
- ✅ **Easier debugging** - All logs in one place
- ✅ **Lower cost** - No Vertex AI charges
- ✅ **Perfect for hackathons and demos** - Fast iteration

**Cons:**
- ⚠️ Larger container size (~2GB)
- ⚠️ Agent and UI scale together
- ⚠️ Updates require full redeployment

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **APIs Enabled**:
   - Cloud Run API
   - Container Registry API
   - BigQuery API (for storm/shelter data)
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
```

**That's it!** No Vertex AI setup needed - everything runs in Cloud Run.

## Step 2: Deploy to Cloud Run

Deploy the complete application:

```bash
# Make the deployment script executable (already done)
chmod +x deploy-cloudrun.sh

# Run the deployment
./deploy-cloudrun.sh
```

The script will:
1. ✅ Validate environment variables
2. 🐳 Build Docker image (multi-stage build)
3. 📤 Push to Google Container Registry
4. 🚀 Deploy to Cloud Run
5. 🌐 Output the public URL

### What Gets Deployed

The Docker container includes:
- **Multi-Agent System** - Your complete `first_responder_agent` with all sub-agents
- **Nginx** - Reverse proxy on port 8080
- **FastAPI** - Agent API server on port 8000 (with AG-UI ADK)
- **Next.js** - UI server on port 3000 (with CopilotKit)
- **Supervisor** - Process manager to run all services

### Deployment Configuration

Default settings (can be modified in `deploy-cloudrun.sh`):
- **Memory**: 2Gi
- **CPU**: 2 vCPUs
- **Timeout**: 300 seconds
- **Max Instances**: 10
- **Min Instances**: 0 (scales to zero when idle)
- **Authentication**: Public (unauthenticated access)

## Step 3: Verify Deployment

Once deployed, you'll receive a URL like:
```
https://first-responder-agent-xxxxx-uc.a.run.app
```

### Test the Deployment

1. **Open the URL** in your browser
2. **Wait for cold start** (first request may take 30-60 seconds)
3. **Test the chat interface** - Try asking: "What disasters are happening in Florida?"
4. **Check the map** - Verify markers appear for locations

### Monitor Logs

```bash
# Tail logs in real-time
gcloud run logs tail first-responder-agent --region us-central1

# View logs in Cloud Console
# https://console.cloud.google.com/run
```

## Troubleshooting

### Container Fails to Start

Check logs for errors:
```bash
gcloud run logs read first-responder-agent --region us-central1 --limit 50
```

Common issues:
- Missing environment variables
- API keys not set correctly
- Docker build failures

### Agent Not Responding

1. Check FastAPI logs in Cloud Run
2. Verify `GOOGLE_API_KEY` is set correctly
3. Check if BigQuery API is enabled
4. Verify agent initialization in logs

### UI Not Loading

1. Check nginx logs in Cloud Run
2. Verify Next.js build succeeded in Docker build logs
3. Check browser console for errors

### Map Not Showing

1. Verify `GOOGLE_MAPS_API_KEY` is set
2. Check that Maps JavaScript API is enabled in GCP Console
3. Verify API key has proper restrictions/permissions

## Updating the Deployment

To deploy updates:

```bash
# Re-run the deployment script
./deploy-cloudrun.sh
```

## Cost Optimization

Cloud Run pricing is based on:
- **CPU/Memory usage** - Only charged when handling requests
- **Request count** - $0.40 per million requests
- **Networking** - Egress charges

Tips to reduce costs:
1. Set `--min-instances=0` to scale to zero when idle
2. Reduce `--memory` and `--cpu` if not needed
3. Set appropriate `--timeout` to avoid long-running requests
4. Use `--max-instances` to cap scaling

## Security Considerations

### Production Deployment Checklist

- [ ] Enable authentication on Cloud Run
- [ ] Restrict API keys to specific domains/IPs
- [ ] Use Secret Manager for sensitive values
- [ ] Enable Cloud Armor for DDoS protection
- [ ] Set up Cloud CDN for static assets
- [ ] Configure custom domain with SSL
- [ ] Enable audit logging
- [ ] Set up monitoring and alerting

### Enable Authentication

To require authentication:

```bash
gcloud run deploy first-responder-agent \
  --no-allow-unauthenticated \
  --region us-central1
```

Then use Identity-Aware Proxy (IAP) or service accounts for access.

## Advanced Configuration

### Custom Domain

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service first-responder-agent \
  --domain your-domain.com \
  --region us-central1
```

### Scaling Configuration

For high-traffic scenarios:

```bash
gcloud run services update first-responder-agent \
  --min-instances=2 \
  --max-instances=100 \
  --concurrency=80 \
  --region us-central1
```

## Next Steps

After successful deployment:
1. Set up monitoring and alerting
2. Configure custom domain
3. Enable authentication for production
4. Set up CI/CD pipeline for automated deployments
5. Implement rate limiting
6. Add caching layer for frequently accessed data

## Need More Scalability?

If you need independent agent scaling or enterprise features, consider [Option B: Vertex AI + Cloud Run](./DEPLOYMENT_VERTEX_AI.md).

