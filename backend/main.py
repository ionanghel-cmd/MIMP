from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="OEM Parts ERP", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creare tabele
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "OEM Parts ERP Backend - Rulează cu succes!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
