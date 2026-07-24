from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Client, Comanda, ComandaPiesa, OrderStatus
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ClientCreate(BaseModel):
    name: str
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

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        db_client = Client(
            nume=client.name,          # ← mapăm name → nume
            telefon=client.telefon,
            email=client.email,
            oras=client.oras,
            tip=client.tip
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comenzi/")
def get_comenzi(db: Session = Depends(get_db)):
    return db.query(Comanda).all()

@router.post("/comenzi/")
def create_comanda(data: ComandaCreate, db: Session = Depends(get_db)):
    try:
        total_cant = sum(p.cantitate for p in data.piese) or 1
        cost_per_unit = data.cost_transport_total / total_cant

        comanda = Comanda(
            client_id=data.client_id,
            cost_transport_total=data.cost_transport_total,
            observatii=data.observatii,
            status=OrderStatus.CERERE
        )
        db.add(comanda)
        db.flush()

        total_vanzare = 0
        total_cost = 0

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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    comenzi = db.query(Comanda).all()
    return {
        "profit_total": round(sum(c.profit or 0 for c in comenzi), 2),
        "comenzi_totale": len(comenzi),
        "in_transport": len([c for c in comenzi if str(c.status) == "In transport"]),
        "clienti": db.query(Client).count()
    }
class ComandaUpdate(BaseModel):
    status: Optional[str] = None
    observatii: Optional[str] = None

@router.put("/comenzi/{comanda_id}")
def update_comanda(comanda_id: str, data: ComandaUpdate, db: Session = Depends(get_db)):
    comanda = db.query(Comanda).filter(Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nu există")

    if data.status:
        # Convertim string-ul în OrderStatus
        try:
            comanda.status = OrderStatus(data.status)
        except Value:
            # Dacă nu e exact enum, încercăm să mapăm
            status_map = {
                "Cerere": OrderStatus.CERERE,
                "Oferta trimisa": OrderStatus.OFERTA,
                "Confirmata": OrderStatus.CONFIRMATA,
                "Comandata la furnizor": OrderStatus.COMANDATA,
                "In transport": OrderStatus.TRANSPORT,
                "Ajunsa": OrderStatus.AJUNSA,
                "Livrata": OrderStatus.LIVRATA,
                "Finalizata": OrderStatus.FINALIZATA,
                "Anulata": OrderStatus.ANULATA,
            }
            comanda.status = status_map.get(data.status, OrderStatus.CERERE)

    if data.observatii is not None:
        comanda.observatii = data.observatii

    db.commit()
    db.refresh(comanda)
    return comanda
