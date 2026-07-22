from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Client, Produs, Comanda
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# ================== CLIENTI ==================
class ClientCreate(BaseModel):
    nume: str
    telefon: str
    email: Optional[str] = None
    oras: Optional[str] = None
    tip: Optional[str] = "persoana"

@router.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    return {"status": "ok", "message": "Dashboard funcționează"}

# Adaugă mai multe rute mai târziu
