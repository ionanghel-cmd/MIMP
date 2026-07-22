from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routes import router
from app.auth import router as auth_router
import uvicorn
import os
import sys
sys.path.insert(0, '/app/backend')

app = FastAPI(title="OEM Parts ERP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Servește frontend
app.mount("/", StaticFiles(directory="/app/frontend/dist", html=True), name="static")

@app.get("/api/")
async def root():
    return {"message": "OEM Parts ERP Backend - Rulează cu succes!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
