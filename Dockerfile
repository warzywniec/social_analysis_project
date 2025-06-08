FROM python:3.11-slim

WORKDIR /app

# Dodaj sqlite3 + inne zależności
RUN apt update && apt install -y sqlite3 libsqlite3-dev gcc


WORKDIR /app
COPY ./app /app/app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
