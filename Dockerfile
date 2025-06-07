# # Oficjalny obraz Pythona
# FROM python:3.11-slim

# # Zmienne środowiskowe
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Katalog roboczy
# WORKDIR /app

# # Kopiuj zależności i zainstaluj
# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Kopiuj całą aplikację
# COPY . .

# # Domyślny port
# EXPOSE 8000

# # Uruchom FastAPI z Uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Dockerfile

FROM python:3.11-slim

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zmienne środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Katalog roboczy
WORKDIR /app

# Kopiuj zależności i instaluj
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopiuj źródła
COPY . .

# Port FastAPI
EXPOSE 8000

# Domyślna komenda
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
