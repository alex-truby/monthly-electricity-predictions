FROM python:3.11-slim-bookworm AS common

EXPOSE 8000

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY models/ ./models/