# Multi-stage build for ADK Agent
FROM python:3.11-slim as builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Create virtual environment
RUN uv venv
RUN . .venv/bin/activate && uv sync --frozen

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Run the agent
CMD ["python", "main.py"]

