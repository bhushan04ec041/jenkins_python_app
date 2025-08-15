FROM python:3.7.0-alpine3.8
RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev netcat-openbsd
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x wait-for-it.sh
ENV FLASK_APP=app.py
CMD ["sh", "wait-for-it.sh", "postgres", "5432", "flask", "run", "--host=0.0.0.0"]