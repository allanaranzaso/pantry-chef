docker_compose := "docker-compose"

run-app:
    poetry run uvicorn pantry_chef.main:app --host 0.0.0.0 --port 8000 --reload

run-docker-app:
    {{ docker_compose }} up -d backend --build

restart-docker-app:
    {{ docker_compose }} restart backend

stop-docker-app:
    {{ docker_compose }} down

build-docker-app:
    {{ docker_compose }} build backend --no-cache
