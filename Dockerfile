# Multi-stage Dockerfile for First Responder Agent
# Runs both FastAPI backend (port 8000) and Next.js UI (port 3000)
# Uses nginx as reverse proxy on port 8080 for Cloud Run

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
# Stage 2: Final Runtime Image
# ============================================
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including Node.js and nginx
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy Python project files
COPY pyproject.toml ./
COPY uv.lock ./

# Copy agent source code (needed before installing dependencies)
COPY first_responder_agent/ ./first_responder_agent/
COPY agent/ ./agent/

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Install Python dependencies
RUN uv pip install --system --no-cache -e .

# Copy UI files
COPY ui/package*.json ./ui/
COPY --from=ui-builder /app/ui/.next ./ui/.next
COPY --from=ui-builder /app/ui/node_modules ./ui/node_modules
COPY ui/public ./ui/public
COPY ui/next.config.ts ./ui/next.config.ts

# Create nginx configuration
RUN mkdir -p /etc/nginx/sites-enabled
COPY <<EOF /etc/nginx/sites-enabled/default
server {
    listen 8080;
    server_name _;

    # FastAPI backend direct access
    location /agent/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8000/health;
    }

    # Next.js UI (handles /api/copilotkit and all other routes)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Create startup script to run all services
COPY <<'EOF' /app/start.sh
#!/bin/bash
set -e

# Start nginx in background
echo "Starting nginx..."
/usr/sbin/nginx -g "daemon off;" &
NGINX_PID=$!

# Start FastAPI in background
cd /app/agent
echo "Starting FastAPI backend..."
PORT=8000 PYTHONUNBUFFERED=1 python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info &
FASTAPI_PID=$!

# Wait for FastAPI to be ready (agent creation takes time)
for i in {1..60}; do
  sleep 1
  if ! kill -0 $FASTAPI_PID 2>/dev/null; then
    exit 1
  fi
  if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
    break
  fi
done

# Start Next.js (foreground)
echo "Starting Next.js UI..."
cd /app/ui
PORT=3000 AGENT_BACKEND_URL=http://localhost:8080/agent/ npm start
EOF

RUN chmod +x /app/start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port (Cloud Run uses PORT env var, defaults to 8080)
EXPOSE 8080

# Run startup script to manage all processes
CMD ["/bin/bash", "/app/start.sh"]

