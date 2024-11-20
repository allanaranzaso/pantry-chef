docker_db_compose := "docker-compose"

create-migration message:
    poetry run alembic revision --autogenerate -m "{{ message }}"

migrate-latest:
    poetry run alembic upgrade head

downgrade-last:
    poetry run alembic downgrade -1

downgrade identifier:
    poetry run alembic downgrade {{ identifier }}

show-migrations:
    poetry run alembic history

docker-migrate:
    {{ docker_db_compose }} exec backend poetry run alembic upgrade head

docker-downgrade identifier:
    {{ docker_db_compose }} exec backend poetry run alembic downgrade {{ identifier }}

docker-show-migrations:
    {{ docker_db_compose }} exec backend poetry run alembic history

run-db-only:
    {{ docker_db_compose }} up db -d --build

restart-db:
    {{ docker_db_compose }} restart db

stop-db:
    {{ docker_db_compose }} stop
