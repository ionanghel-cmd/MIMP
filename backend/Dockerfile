FROM python:3.11-slim

WORKDIR /app

# Copiază requirements
COPY backend/requirements.txt .

# Instalează
RUN pip install --no-cache-dir -r requirements.txt

# Copiază tot backend-ul
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
