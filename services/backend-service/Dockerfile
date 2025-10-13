# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy Poetry configuration files from project root
COPY pyproject.toml poetry.lock ./

# Configure Poetry to not create virtualenvs inside the container
RUN poetry config virtualenvs.create false

# Install dependencies (only runtime, no dev)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application code
COPY services/backend-service/app ./app
COPY shared ./shared

# Expose port
EXPOSE 8002

# Set environment variables
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
