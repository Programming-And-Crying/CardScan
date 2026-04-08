FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install uv && uv pip install --system -e .
COPY . /app
WORKDIR /app/app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
