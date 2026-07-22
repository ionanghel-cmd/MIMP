FROM python:3.11-slim

WORKDIR /app

# Backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Frontend
COPY frontend/package*.json frontend/
RUN apt-get update && apt-get install -y nodejs npm && cd frontend && npm install

COPY Frontend/ ./frontend/
RUN cd frontend && npm run build

# Copiază backend cod
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
