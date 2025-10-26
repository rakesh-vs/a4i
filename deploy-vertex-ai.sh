#!/bin/bash
# Deploy First Responder Agent using Option B: Vertex AI Agent Engine + Cloud Run UI
# This script deploys in two stages:
#   1. Agent backend to Vertex AI Agent Engine
#   2. FastAPI + Next.js UI to Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 First Responder Agent - Vertex AI + Cloud Run Deployment${NC}"
echo "================================================================"
echo ""
echo "This will deploy your application in two stages:"
echo "  ${BLUE}Stage 1:${NC} Agent backend → Vertex AI Agent Engine"
echo "  ${BLUE}Stage 2:${NC} FastAPI + UI → Cloud Run"
echo ""

# Load environment variables from .env file
if [ -f .env ]; then
    echo -e "${GREEN}✓${NC} Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}✗${NC} .env file not found!"
    echo "Please create a .env file with the following variables:"
    echo "  GCP_PROJECT=your-project-id"
    echo "  GCP_REGION=us-central1"
    echo "  GOOGLE_API_KEY=your-api-key"
    echo "  GOOGLE_MAPS_API_KEY=your-maps-api-key"
    echo "  STAGING_BUCKET=gs://your-bucket"
    exit 1
fi

# Validate required environment variables
REQUIRED_VARS=("GCP_PROJECT" "GCP_REGION" "GOOGLE_API_KEY" "GOOGLE_MAPS_API_KEY" "STAGING_BUCKET")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}✗${NC} Missing required environment variable: $var"
        exit 1
    fi
done

echo -e "${GREEN}✓${NC} All required environment variables found"

# Configuration
SERVICE_NAME="first-responder-agent-ui"
IMAGE_NAME="gcr.io/${GCP_PROJECT}/${SERVICE_NAME}"
MEMORY="2Gi"
CPU="2"
MAX_INSTANCES="10"
MIN_INSTANCES="0"
TIMEOUT="300s"

echo ""
echo "Deployment Configuration:"
echo "  Project: ${GCP_PROJECT}"
echo "  Region: ${GCP_REGION}"
echo "  Service: ${SERVICE_NAME}"
echo "  Image: ${IMAGE_NAME}"
echo ""

# Confirm deployment
read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

# ============================================
# STAGE 1: Deploy Agent to Vertex AI
# ============================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}STAGE 1: Deploying Agent Backend to Vertex AI Agent Engine${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Running: python deploy.py"
python deploy.py

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Agent deployment to Vertex AI failed!"
    exit 1
fi

echo ""
echo -e "${GREEN}✓${NC} Agent deployed to Vertex AI successfully"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Copy the RESOURCE_NAME from the output above${NC}"
echo -e "${YELLOW}   and add it to your .env file:${NC}"
echo -e "${YELLOW}   RESOURCE_NAME=projects/.../locations/.../reasoningEngines/...${NC}"
echo ""
read -p "Have you updated .env with RESOURCE_NAME? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Please update .env with RESOURCE_NAME and run this script again${NC}"
    exit 0
fi

# Reload .env to get RESOURCE_NAME
export $(cat .env | grep -v '^#' | xargs)

if [ -z "$RESOURCE_NAME" ]; then
    echo -e "${RED}✗${NC} RESOURCE_NAME not found in .env file!"
    echo "Please add RESOURCE_NAME to .env and run this script again"
    exit 1
fi

echo -e "${GREEN}✓${NC} RESOURCE_NAME found: ${RESOURCE_NAME}"

# ============================================
# STAGE 2: Build and Deploy UI to Cloud Run
# ============================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}STAGE 2: Building and Deploying UI to Cloud Run${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create a temporary Dockerfile for UI-only deployment
echo "Creating Dockerfile for UI deployment..."
cat > Dockerfile.vertex-ai << 'EOF'
# Dockerfile for Option B: UI only (agent runs on Vertex AI)
# This is a lighter container that only runs FastAPI wrapper + Next.js UI

# ============================================
# Stage 1: Build Next.js Frontend
# ============================================
FROM node:20-alpine AS ui-builder

WORKDIR /app/ui

# Copy package files
COPY ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy UI source code
COPY ui/ ./

# Build Next.js app for production
RUN npm run build

# ============================================
# Stage 2: Final Runtime Image (UI Only)
# ============================================
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including Node.js and nginx
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nginx \
    supervisor \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python project files (minimal dependencies for API wrapper only)
COPY pyproject.toml ./
COPY uv.lock ./

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system --no-cache -e .

# Copy ONLY the agent wrapper (not the full agent logic)
COPY agent/ ./agent/

# Copy UI files
COPY ui/package*.json ./ui/
COPY --from=ui-builder /app/ui/.next ./ui/.next
COPY --from=ui-builder /app/ui/node_modules ./ui/node_modules
COPY ui/public ./ui/public
COPY ui/next.config.ts ./ui/next.config.ts

# Create nginx configuration
RUN mkdir -p /etc/nginx/sites-enabled
COPY <<'NGINX_EOF' /etc/nginx/sites-enabled/default
server {
    listen 8080;
    server_name _;

    # Next.js UI (main app)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # FastAPI backend (for CopilotKit API route)
    location /api/agent/ {
        rewrite ^/api/agent/(.*) /$1 break;
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8000/health;
    }
}
NGINX_EOF

# Create supervisor configuration
COPY <<'SUPERVISOR_EOF' /etc/supervisor/conf.d/supervisord.conf
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:fastapi]
command=python agent/main.py
directory=/app
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
environment=PORT="8000",PYTHONUNBUFFERED="1"

[program:nextjs]
command=npm start
directory=/app/ui
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
environment=PORT="3000"
SUPERVISOR_EOF

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run supervisor to manage all processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
EOF

echo -e "${GREEN}✓${NC} Dockerfile created"

# Step 1: Build the Docker image
echo ""
echo "Building Docker image..."
docker build -f Dockerfile.vertex-ai -t ${IMAGE_NAME}:latest .

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Docker build failed!"
    rm Dockerfile.vertex-ai
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker image built successfully"

# Step 2: Push to Google Container Registry
echo ""
echo "Pushing image to Google Container Registry..."
docker push ${IMAGE_NAME}:latest

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Docker push failed!"
    rm Dockerfile.vertex-ai
    exit 1
fi
echo -e "${GREEN}✓${NC} Image pushed successfully"

# Step 3: Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME}:latest \
    --platform managed \
    --region ${GCP_REGION} \
    --project ${GCP_PROJECT} \
    --allow-unauthenticated \
    --memory ${MEMORY} \
    --cpu ${CPU} \
    --timeout ${TIMEOUT} \
    --max-instances ${MAX_INSTANCES} \
    --min-instances ${MIN_INSTANCES} \
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY},GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY},GCP_PROJECT=${GCP_PROJECT},GCP_REGION=${GCP_REGION},RESOURCE_NAME=${RESOURCE_NAME},STAGING_BUCKET=${STAGING_BUCKET},AGENT_BACKEND_URL=http://localhost:8000/,NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}" \
    --port 8080

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Cloud Run deployment failed!"
    rm Dockerfile.vertex-ai
    exit 1
fi

# Clean up temporary Dockerfile
rm Dockerfile.vertex-ai

# Step 4: Get the service URL
echo ""
echo "Getting service URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${GCP_REGION} \
    --project ${GCP_PROJECT} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}================================================================"
echo "🎉 Deployment Successful!"
echo "================================================================${NC}"
echo ""
echo -e "${BLUE}Architecture:${NC}"
echo "  ✓ Agent Backend → Vertex AI Agent Engine"
echo "  ✓ FastAPI + UI → Cloud Run"
echo ""
echo -e "${BLUE}Service URL:${NC} ${SERVICE_URL}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Open the URL in your browser"
echo "  2. Test the chat interface"
echo "  3. Monitor Cloud Run logs: gcloud run logs tail ${SERVICE_NAME} --region ${GCP_REGION}"
echo "  4. Monitor Vertex AI logs: https://console.cloud.google.com/logs"
echo ""
echo -e "${YELLOW}Note: First request may take 30-60 seconds as the container starts${NC}"
echo ""

