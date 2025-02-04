# Pantry Chef

Welcome to Pantry Chef, a FastAPI-based backend application designed to help users manage
their pantry items and discover recipes.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **FastAPI Framework**: Utilizes FastAPI for building robust and high-performance APIs.
- **Dockerized Environment**: Containerized using Docker for consistent development and
  deployment.
- **Recipe Management**: Allows users to search and manage recipes based on available
  pantry items.
- (TBD) **User Authentication**: Implements JWT-based authentication for secure user
  sessions.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started): To run the application in a containerized
  environment.
- [Git](https://git-scm.com/): To clone the repository.
- Install Just via homebrew(better version
  control) - [casey/just: 🤖 Just a command runner (github.com)](https://github.com/casey/just)
    - Note for ease of daily development, alot of commands are masked within just. But
      please feel free to dive into the just files(`justfile` and `.just` directory) to
      get a better understanding of what is under the hood.
- Install Pipx via
  homebrew - [pypa/pipx: Install and Run Python Applications in Isolated Environments (github.com)](https://github.com/pypa/pipx)
    - Pipx will be used to install any global tool like Poetry

- Install Poetry via
  Pipx - [Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/#installing-with-pipx)

- Install pyenv via
  homebrew - [pyenv/pyenv: Simple Python version management (github.com)](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/allanaranzaso/pantry-chef.git
   cd pantry-chef
   ```

2. **Set Up Environment Variables**:

   Create a `.env` file in the app directory and configure the necessary environment
   variables. For example:

   ```env
   DB_USERNAME=user
   DB_PASSWORD=password
   ```

   Ensure you replace `user`, `password`, with your actual database credentials and
   desired database name.

### Setting up Dependencies

- Install Pre-commit and initialise it via
  `pre-commit install --hook-type pre-commit --hook-type pre-push`
- Navigate to the `app` folder
- Install Python 3.12.x
  ```
  pyenv install 3.12.x
  ```
- Set local python environment
  ```
  pyenv local 3.12.x
  ```
- Set poetry config `virtualenvs.in-project` to `true` via
  ```
  poetry config virtualenvs.in-project true
  ```
- Ensure poetry is using the correct environment via
  ```
  poetry env use 3.12.x
  ```
- Ensure the correct python version is using within the local dev env by running the
  command below and make sure 3.12.x is used
  ```
  poetry run python --version
  ```
- Install the project via
  ```
  poetry install
  ```

### Running the Application

- Copy the .env.sample file as .env
    ```
    cp .env.sample .env
    ```

**Using Docker**:

1. **Run the below command to build and start the server**:

   ```bash
   just run-app
   ```

2. **Run the initial database migration**:

   ```bash
   just docker-migrate
   ```

   The application will be accessible at `http://localhost:8000`.

## API Documentation

Interactive API documentation is available via Swagger UI. Once the application is
running, navigate to:

- Swagger UI: `http://localhost:8000/docs`

These interfaces provide detailed information about the available endpoints,
request/response schemas, and allow for testing the API directly from the browser.

## Project Structure

```bash
pantry-chef/
├── app/
│   ├── pantry_chef/
│       ├──── ingredient/
│       │     ├──── api.py
│       │     ├──── crud.py
│       │     ├──── model.py
│       │     ├──── schema.py
│       │     ├──── services.py
│       ├──── instruction/
│       ├──── recipe/
│       └── ...
├── tests/
├── alembic/
├── Dockerfile
├── pyproject.toml
├── .env.sample
└── README.md
```

- `app/`: Contains the main application code.
    - `*/api.py`: Defines the API routes.
    - `*/crud.py`: Defines CRUD operations for the resource.
    - `*/models.py`: SQLAlchemy models for the database tables.
    - `*/schemas.py`: Pydantic schemas for data validation.
    - `*/services.py`: Business logic and service layers.
    - `main.py`: Entry point of the application.
- `tests/`: Contains test cases for the application.
- `alembic/`: Database migration scripts.
- `Dockerfile`: Instructions to build the Docker image.
- `pyproject.toml`: Python dependencies.
- `.env.sample`: Sample environment variables file.
- `README.md`: Project documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more
details.

---

*Note: This project is a part of my personal portfolio and is intended to demonstrate my
skills in software development, particularly in building and deploying backend
applications using FastAPI and Docker.*
