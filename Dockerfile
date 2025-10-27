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

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1

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

# Set Python to unbuffered mode globally
ENV PYTHONUNBUFFERED=1

# Install Node.js runtime for frontend, curl for health checks, and procps for process management
RUN apt-get update && apt-get install -y nodejs npm curl procps && rm -rf /var/lib/apt/lists/*

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

  # Test if we can import the app
  echo "   Testing if main.py can be imported..."
  python -c "import sys; sys.path.insert(0, '/agent'); from main import app; print('✅ App imported successfully')" 2>&1

  if [ $? -ne 0 ]; then
    echo "❌ Failed to import app! Backend will not start."
    exit 1
  fi

  echo "   Starting backend with python main.py..."
  # Run main.py directly which will start uvicorn, redirect all output to stdout/stderr
  python main.py 2>&1 &
else
  echo "⚠️  Virtual environment not found at /agent/.venv"
  exit 1
fi

BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 5

# Check if backend is responding
echo "🔍 Testing backend health..."
for i in {1..10}; do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is responding!"
    break
  fi
  if [ $i -eq 10 ]; then
    echo "⚠️  Backend health check failed after 10 attempts"
    echo "   Checking if process is still running..."
    if ps -p $BACKEND_PID > /dev/null; then
      echo "   Process is running but not responding"
    else
      echo "   Process has died!"
      exit 1
    fi
  fi
  sleep 1
done

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

