# --- Stage 1: Base Image ---
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the Flask port
EXPOSE 5001

# Use unbuffered output so logs appear immediately
ENV PYTHONUNBUFFERED=1

# Run Flask app
CMD ["python", "-u", "app.py"]