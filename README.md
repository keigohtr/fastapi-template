# fastapi-template
This is the template project of FastAPI application.

This project includes the following tech stacks.
- FastAPI + MySQL
- Alembic
- Github Actions
- Helm chart

## How to Run
```shell
docker-compose up
```

Redoc (-> OpenAPI Spec) is avalable on <http://localhost:5000/redoc>

## How to generate a DB migration script
```shell
docker-compose stop
docker-compose rm
docker volume rm fastapi-template_mysql-db
docker-compose run app make alembic_revision
```

## fmt
```shell
docker-compose run app make fmt
```

## Lint
```shell
docker-compose run app make lint
```

## Test
```shell
docker-compose run app make test
```

## Cleanup
```shell
docker-compose stop
docker-compose rm
docker volume rm fastapi-template_mysql-db
```
