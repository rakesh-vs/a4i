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

    # Next.js UI (main app)
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

    # FastAPI backend (for CopilotKit API route)
    location /api/agent/ {
        rewrite ^/api/agent/(.*) /\$1 break;
        proxy_pass http://localhost:8000;
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
}
EOF

# Create startup script to run all services
COPY <<'EOF' /app/start.sh
#!/bin/bash
set -e

# Start nginx in background
echo "Starting nginx..."
/usr/sbin/nginx -g "daemon off;" &

# Start FastAPI in background
echo "Starting FastAPI backend..."
cd /app
PORT=8000 python agent/main.py &

# Start Next.js (foreground - this keeps the container running)
echo "Starting Next.js UI..."
cd /app/ui
PORT=3000 npm start
EOF

RUN chmod +x /app/start.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port (Cloud Run uses PORT env var, defaults to 8080)
EXPOSE 8080

# Run startup script to manage all processes
CMD ["/bin/bash", "/app/start.sh"]

