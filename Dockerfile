FROM python:3.9

WORKDIR /app/

COPY requirements.txt ./
COPY .env ./
COPY alembic.ini ./

RUN pip install -r requirements.txt



