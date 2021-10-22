mypy:
	poetry run mypy app

lint: mypy
	poetry run flake8 app tests --max-line-length=120 --exclude=.venv,venv

fmt:
	poetry run isort -rc -sl app tests
	poetry run autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables app tests
	poetry run black app tests
	poetry run isort -rc -m 3 app tests

test:
	poetry run pytest -v -n 2 --cov=app tests/

prestart:
	poetry run python scripts/pre_start.py
	poetry run alembic upgrade head

start: prestart
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload

alembic_revision: prestart
	poetry run alembic revision --autogenerate
