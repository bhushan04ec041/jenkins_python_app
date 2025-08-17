# --- Stage 1: Base Image ---
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (psycopg2 etc.)
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
