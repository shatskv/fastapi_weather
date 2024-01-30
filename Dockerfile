FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk upgrade \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && pip install --upgrade pip

COPY /weather /app/weather

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --without dev 

CMD ["uvicorn", "weather.server:app", "--host", "0.0.0.0", "--port", "8000"]
