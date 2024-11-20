docker_compose := "docker-compose"

run-app:
    poetry run uvicorn finding_capture.main:app --host 0.0.0.0 --port 8000 --reload

run-docker-app:
    {{ docker_compose }} up -d --build

restart-docker-app:
    {{ docker_compose }} restart

stop-docker-app:
    {{ docker_compose }} stop

build-docker-app:
    {{ docker_compose }} build --no-cache
