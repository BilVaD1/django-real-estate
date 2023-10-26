# This checks if a file named .env exists in the current directory.
# If it does, it includes the variables from that file, exporting them for subprocesses.
# It also sets ENV_FILE_PARAM for Docker commands to use the .env file.
ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif

build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

show-logs:
	docker compose logs

# docker compose exec api - execute command inside the docker where api it's name of container
migrate:
	docker compose exec api python3 manage.py migrate

makemigrations:
	docker compose exec api python3 manage.py makemigrations

superuser:
	docker compose exec api python3 manage.py createsuperuser

collectstatic:
	docker compose exec api python3 manage.py collectstatic --no-input --clear

# Donw the container and remove the volumes
down-v:
	docker compose down -v

volume:
	docker volume inspect estate-src_postgres_data

estate-db:
	docker compose exec postgres-db psql --username=admin --dbname=estate

test:
	docker compose exec api pytest -p no:warnings --cov=.

test-html:
	docker compose exec api pytest -p no:warnings --cov=. --cov-report html

# Check code against style conventions using flake8
flake8:
	docker compose exec api flake8 .

# Check code formatting using Black without making changes
black-check:
	docker compose exec api black --check --exclude=migrations .

# Show the diff of code formatting changes using Black
black-diff:
	docker compose exec api black --diff --exclude=migrations .

# Format code using Black
black:
	docker compose exec api black --exclude=migrations .

# Check import sorting using isort without making changes
isort-check:
	docker compose exec api isort . --check-only --skip env --skip migrations

# Show the diff of import sorting changes using isort
isort-diff:
	docker compose exec api isort . --diff --skip env --skip migrations

# Sort imports using isort
isort:
	docker compose exec api isort . --skip env --skip migrations
