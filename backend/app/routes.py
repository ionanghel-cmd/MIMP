from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Client, Comanda, ComandaPiesa, OrderStatus
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import uuid

router = APIRouter()

# ========== SCHEMAS ==========
class ClientCreate(BaseModel):
    nume: str
    telefon: str
    email: Optional[str] = None
    oras: Optional[str] = None
    tip: Optional[str] = "persoana"

class PiesaCreate(BaseModel):
    cod_oem: str
    denumire: str
    cantitate: int = 1
    pret_cumparare: float
    pret_vanzare: float

class ComandaCreate(BaseModel):
    client_id: str
    cost_transport_total: float
    observatii: Optional[str] = None
    piese: List[PiesaCreate]

# ========== CLIENTI ==========
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

# ========== COMENZI ==========
@router.post("/comenzi/")
def create_comanda(data: ComandaCreate, db: Session = Depends(get_db)):
    # Verifică client
    client = db.query(Client).filter(Client.id == data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Clientul nu există")

    # Alocare automată transport (după cantitate)
    total_cantitate = sum(p.cantitate for p in data.piese) or 1
    cost_per_unit = data.cost_transport_total / total_cantitate

    total_vanzare = 0
    total_cost = 0

    comanda = Comanda(
        client_id=data.client_id,
        cost_transport_total=data.cost_transport_total,
        observatii=data.observatii,
        status=OrderStatus.CERERE
    )
    db.add(comanda)
    db.flush()  # ca să avem ID

    for p in data.piese:
        cost_livrare = round(cost_per_unit * p.cantitate, 2)
        profit = round((p.pret_vanzare - p.pret_cumparare - cost_livrare) * p.cantitate, 2)

        piesa = ComandaPiesa(
            comanda_id=comanda.id,
            cod_oem=p.cod_oem,
            denumire=p.denumire,
            cantitate=p.cantitate,
            pret_cumparare=p.pret_cumparare,
            cost_livrare=cost_livrare,
            pret_vanzare=p.pret_vanzare,
            profit=profit
        )
        db.add(piesa)

        total_vanzare += p.pret_vanzare * p.cantitate
        total_cost += (p.pret_cumparare + cost_livrare) * p.cantitate

    comanda.total_vanzare = round(total_vanzare, 2)
    comanda.total_cost = round(total_cost, 2)
    comanda.profit = round(total_vanzare - total_cost, 2)

    db.commit()
    db.refresh(comanda)
    return comanda

@router.get("/comenzi/")
def get_comenzi(db: Session = Depends(get_db)):
    return db.query(Comanda).order_by(Comanda.data.desc()).all()

@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    comenzi = db.query(Comanda).all()
    return {
        "profit_total": sum(c.profit or 0 for c in comenzi),
        "comenzi_totale": len(comenzi),
        "in_transport": len([c for c in comenzi if c.status == OrderStatus.TRANSPORT]),
        "clienti_noi": db.query(Client).count()
    }
