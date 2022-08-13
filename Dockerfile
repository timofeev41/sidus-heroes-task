FROM python:3.10-slim-buster as requirements-stage
EXPOSE 8000
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
RUN apt update
WORKDIR /src/
COPY --from=requirements-stage /tmp/requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY . .
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]