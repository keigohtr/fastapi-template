FROM python:3.8 AS production

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.toml /app/poetry.toml
COPY ./poetry.lock /app/poetry.lock
COPY . /app

WORKDIR /app
ENV PYTHONPATH /app

RUN pip install pip -U \
    && pip install poetry \
    && cd /app \
    && poetry install --no-dev \
    && pip uninstall poetry -y

EXPOSE 5000
CMD /bin/bash -c "uvicorn app.main:app --host 0.0.0.0 --port 5000"


FROM production AS development

RUN pip install poetry \
    && cd /app \
    && poetry install
