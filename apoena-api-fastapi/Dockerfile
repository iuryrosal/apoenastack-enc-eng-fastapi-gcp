FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /apoena_api_fastapi

COPY pyproject.toml poetry.lock ./
COPY apoena_api_fastapi ./apoena_api_fastapi
RUN touch README.md

RUN poetry install --without dev

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "fastapi", "run", "apoena_api_fastapi/app.py", "--port", "8080"]