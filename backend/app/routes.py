from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Client, Comanda, ComandaPiesa, OrderStatus
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

# ==================== SCHEMAS ====================
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

# ==================== CLIENTI ====================
@router.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Verifică dacă telefonul există deja
    existing = db.query(Client).filter(Client.telefon == client.telefon).first()
    if existing:
        raise HTTPException(status_code=400, detail="Există deja un client cu acest telefon")
    
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.nume).all()

# ==================== COMENZI ====================
@router.post("/comenzi/")
def create_comanda(data: ComandaCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Clientul nu există")

    if not data.piese:
        raise HTTPException(status_code=400, detail="Trebuie să adaugi cel puțin o piesă")

    # Alocare automată cost transport după cantitate
    total_cantitate = sum(p.cantitate for p in data.piese) or 1
    cost_per_unit = data.cost_transport_total / total_cantitate

    total_vanzare = 0.0
    total_cost = 0.0

    comanda = Comanda(
        client_id=data.client_id,
        cost_transport_total=data.cost_transport_total,
        observatii=data.observatii,
        status=OrderStatus.CERERE
    )
    db.add(comanda)
    db.flush()

    for p in data.piese:
        cost_livrare = round(cost_per_unit * p.cantitate, 2)
        profit_piesa = round((p.pret_vanzare - p.pret_cumparare - cost_livrare) * p.cantitate, 2)

        piesa = ComandaPiesa(
            comanda_id=comanda.id,
            cod_oem=p.cod_oem,
            denumire=p.denumire,
            cantitate=p.cantitate,
            pret_cumparare=p.pret_cumparare,
            cost_livrare=cost_livrare,
            pret_vanzare=p.pret_vanzare,
            profit=profit_piesa
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
        "profit_total": round(sum(c.profit or 0 for c in comenzi), 2),
        "comenzi_totale": len(comenzi),
        "in_transport": len([c for c in comenzi if c.status == OrderStatus.TRANSPORT]),
        "clienti": db.query(Client).count()
    }
