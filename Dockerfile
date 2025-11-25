FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (no virtualenvs inside Docker)
ENV POETRY_VERSION=2.2.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

# Set work directory
WORKDIR /app

# Copy only dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy app code
COPY . .

WORKDIR /app/src

# Set environment variables for Flask
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    TEST_ENV=false

# Default command: run gunicorn with 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]
