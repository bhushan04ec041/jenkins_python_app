FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and scripts
COPY . .
COPY wait-for-it.sh .
COPY start.sh .

# Make scripts executable
RUN chmod +x wait-for-it.sh start.sh

ENV PYTHONUNBUFFERED=1
EXPOSE 5001

# Start container via start.sh
CMD ["./start.sh"]
