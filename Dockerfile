# syntax=docker/dockerfile:1

# --- Frontend Builder ---
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy UI source code
COPY ui/ ./

# Build Next.js app
RUN npm run build

# --- Backend Builder ---
FROM python:3.12-slim AS backend-builder

WORKDIR /agent

# Install uv
RUN pip install uv

# Copy dependency files and source code
COPY pyproject.toml uv.lock ./
COPY first_responder_agent ./first_responder_agent
COPY agent ./agent

RUN uv sync --frozen --no-dev

# --- Runtime image ---
FROM python:3.12-slim

WORKDIR /app

# Install Node.js runtime for frontend
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy backend code first
COPY agent/ /agent/
COPY first_responder_agent/ /agent/first_responder_agent/
COPY pyproject.toml /agent/

# Copy backend virtual environment (after code to avoid being overwritten)
COPY --from=backend-builder /agent/.venv /agent/.venv

# Copy frontend build output
COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /app/frontend/package.json
COPY --from=frontend-builder /app/frontend/node_modules /app/frontend/node_modules
COPY ui/next.config.ts /app/frontend/next.config.ts

# Create startup script
RUN mkdir -p /app/scripts
COPY <<'EOF' /app/scripts/start.sh
#!/bin/bash
set -e

echo "=========================================="
echo "First Responder Agent - Starting Services"
echo "=========================================="
echo ""

# Verify GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
  echo "❌ ERROR: GOOGLE_API_KEY is not set!"
  echo "   Please set GOOGLE_API_KEY as an environment variable"
  exit 1
fi

echo "✅ GOOGLE_API_KEY is set"
echo ""

# Start backend API server
echo "🚀 Starting backend API server..."
cd /agent

# Activate virtual environment and start backend
if [ -f /agent/.venv/bin/activate ]; then
  source /agent/.venv/bin/activate
  python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
else
  echo "⚠️  Virtual environment not found at /agent/.venv"
  exit 1
fi

BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Start frontend
echo "🚀 Starting frontend..."
cd /app/frontend
npm start &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "=========================================="
echo "✅ Services Started Successfully!"
echo "=========================================="
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
EOF

RUN chmod +x /app/scripts/start.sh

EXPOSE 3000 8000

# Environment variables (set these at runtime for security)
# GOOGLE_API_KEY - Required: Your Google API key
# GOOGLE_MAPS_API_KEY - Required: Your Google Maps API key
# GCP_PROJECT - Required: Your GCP project ID
# GCP_REGION - Required: GCP region (e.g., us-central1)

ENV BACKEND_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=http://localhost:8000
ENV AGENT_BACKEND_URL=http://localhost:8000/

CMD ["/app/scripts/start.sh"]

