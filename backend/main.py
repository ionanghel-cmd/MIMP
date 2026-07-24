from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
import app.models   # ← FOARTE IMPORTANT - încarcă modelele
from app.routes import router
import os

app = FastAPI(title="OEM Parts ERP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

app.include_router(router, prefix="/api")

if os.path.exists("/app/frontend/dist"):
    app.mount("/", StaticFiles(directory="/app/frontend/dist", html=True), name="static")

@app.get("/api/")
async def root():
    return {"message": "OEM Parts ERP Backend - Rulează cu succes!"}
