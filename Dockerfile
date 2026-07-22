FROM python:3.11-slim

# Setează working directory
WORKDIR /app

# Copiază doar requirements întâi (pentru cache mai bun)
COPY backend/requirements.txt .

# Instalează dependințele
RUN pip install --no-cache-dir -r requirements.txt

# Copiază restul codului backend
COPY backend/ .

# Expune portul
EXPOSE 8000

# Rulează aplicația
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
