#!/bin/bash
# Deploy First Responder Agent to Google Cloud Run
# This script builds and deploys the complete application (Agent + FastAPI + Next.js UI) in a single container

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 First Responder Agent - Cloud Run Deployment${NC}"
echo "=================================================="
echo ""
echo "This will deploy your complete application to Cloud Run:"
echo "  ✓ Multi-agent system (first_responder_agent)"
echo "  ✓ FastAPI backend (AG-UI ADK)"
echo "  ✓ Next.js UI (CopilotKit)"
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
    exit 1
fi

# Validate required environment variables
REQUIRED_VARS=("GCP_PROJECT" "GCP_REGION" "GOOGLE_API_KEY" "GOOGLE_MAPS_API_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}✗${NC} Missing required environment variable: $var"
        exit 1
    fi
done

echo -e "${GREEN}✓${NC} All required environment variables found"

# Configuration
SERVICE_NAME="first-responder-agent"
IMAGE_NAME="gcr.io/${GCP_PROJECT}/${SERVICE_NAME}"
MEMORY="2Gi"
CPU="2"
MAX_INSTANCES="8"
MIN_INSTANCES="0"
TIMEOUT="300s"

echo ""
echo "Deployment Configuration:"
echo "  Project: ${GCP_PROJECT}"
echo "  Region: ${GCP_REGION}"
echo "  Service: ${SERVICE_NAME}"
echo "  Image: ${IMAGE_NAME}"
echo "  Memory: ${MEMORY}"
echo "  CPU: ${CPU}"
echo ""

# Confirm deployment
read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

# Step 1: Build the Docker image
echo ""
echo -e "${GREEN}Step 1: Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:latest .

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Docker build failed!"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker image built successfully"

# Step 2: Push to Google Container Registry
echo ""
echo -e "${GREEN}Step 2: Pushing image to Google Container Registry...${NC}"
docker push ${IMAGE_NAME}:latest

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Docker push failed!"
    exit 1
fi
echo -e "${GREEN}✓${NC} Image pushed successfully"

# Step 3: Deploy to Cloud Run
echo ""
echo -e "${GREEN}Step 3: Deploying to Cloud Run...${NC}"
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
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY},GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY},GCP_PROJECT=${GCP_PROJECT},GCP_REGION=${GCP_REGION},AGENT_BACKEND_URL=http://localhost:8000/,NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}" \
    --port 8080

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Cloud Run deployment failed!"
    exit 1
fi

# Step 4: Get the service URL
echo ""
echo -e "${GREEN}Step 4: Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${GCP_REGION} \
    --project ${GCP_PROJECT} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}=================================================="
echo "🎉 Deployment Successful!"
echo "==================================================${NC}"
echo ""
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Next steps:"
echo "  1. Open the URL in your browser"
echo "  2. Test the chat interface"
echo "  3. Monitor logs: gcloud run logs tail ${SERVICE_NAME} --region ${GCP_REGION}"
echo ""
echo -e "${YELLOW}Note: First request may take 30-60 seconds as the container starts${NC}"
echo ""

