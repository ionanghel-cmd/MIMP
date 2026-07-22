FROM python:3.11-slim

WORKDIR /app

# Copiază tot
COPY . /app

# Backend
RUN pip install --no-cache-dir -r backend/requirements.txt

# Frontend
RUN apt-get update && apt-get install -y nodejs npm && \
    cd frontend && npm install && npm run build

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
