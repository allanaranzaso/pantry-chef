# Use the slim version of Python for a lightweight, more compatible base image
FROM python:3.12-slim

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install curl and make necessary directories
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install the dependencies with poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code to the container
COPY . /app

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "pantry_chef.main:app", "--host", "0.0.0.0", "--port", "8000"]
