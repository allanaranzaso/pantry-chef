# Use the slim version of Python for a lightweight, more compatible base image
FROM python:3.12-slim AS base

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8.1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME="/opt/poetry" \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install curl and make necessary directories
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.1

# Set the working directory inside the container
RUN mkdir -p /pantry-chef-backend/pantry_chef
WORKDIR /pantry-chef-backend

FROM base AS builder

WORKDIR /pantry-chef-backend

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the dependencies with poetry
RUN poetry install --with ci

FROM builder AS dev_base

# Copy the rest of the application code to the container
COPY . .

COPY --from=builder /pantry-chef-backend/.venv ./.venv

# Expose the port on which FastAPI will run
EXPOSE 8000
EXPOSE 5432

# Command to run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "pantry_chef.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
