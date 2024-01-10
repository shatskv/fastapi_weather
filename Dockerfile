FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk upgrade \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && pip install --upgrade pip

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY weather_api.py /app

CMD ["python", "weather_api.py"]

