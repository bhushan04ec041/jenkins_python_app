FROM python:3.7.0-alpine3.8

# Install build dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    python3-dev \
    build-base

# Set working directory
WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5001

# Run the Flask app
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
CMD ["sh", "wait-for-it.sh", "postgres", "5432", "flask", "run", "--host=0.0.0.0", "--port=5001"]