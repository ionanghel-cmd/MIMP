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

class ComandaUpdate(BaseModel):
    status: Optional[str] = None
    observatii: Optional[str] = None

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        db_client = Client(
            nume=client.name,
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
    comenzi = db.query(Comanda).order_by(Comanda.data.desc()).all()
   
    result = []
    for c in comenzi:
        client = db.query(Client).filter(Client.id == c.client_id).first()
        piese = db.query(ComandaPiesa).filter(ComandaPiesa.comanda_id == c.id).all()
       
        result.append({
            "id": str(c.id),
            "numar": c.numar,
            "data": str(c.data),
            "status": c.status.value if c.status else "Cerere",
            "observatii": c.observatii,
            "cost_transport_total": c.cost_transport_total,
            "total_vanzare": c.total_vanzare,
            "total_cost": c.total_cost,
            "profit": c.profit,
            "client_nume": client.nume if client else "Necunoscut",
            "client_telefon": client.telefon if client else "",
            "piese": [
                {
                    "cod_oem": p.cod_oem,
                    "denumire": p.denumire,
                    "cantitate": p.cantitate,
                    "pret_cumparare": p.pret_cumparare,
                    "cost_livrare": p.cost_livrare,
                    "pret_vanzare": p.pret_vanzare,
                    "profit": p.profit
                } for p in piese
            ]
        })
    return result

@router.post("/comenzi/")
def create_comanda(data: ComandaCreate, db: Session = Depends(get_db)):
    try:
        # Generăm numărul următor (începe de la 1000)
        last = db.query(Comanda).order_by(Comanda.numar.desc()).first()
        next_numar = (last.numar + 1) if last and last.numar else 1000

        total_cant = sum(p.cantitate for p in data.piese) or 1
        cost_per_unit = data.cost_transport_total / total_cant

        comanda = Comanda(
            numar=next_numar,
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

@router.put("/comenzi/{comanda_id}")
def update_comanda(comanda_id: str, data: ComandaUpdate, db: Session = Depends(get_db)):
    comanda = db.query(Comanda).filter(Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nu există")

    if data.status:
        try:
            comanda.status = OrderStatus(data.status)
        except ValueError:
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

@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    comenzi = db.query(Comanda).all()
    return {
        "profit_total": round(sum(c.profit or 0 for c in comenzi), 2),
        "comenzi_totale": len(comenzi),
        "in_transport": len([c for c in comenzi if str(c.status) == "In transport"]),
        "clienti": db.query(Client).count()
    }
@router.delete("/comenzi/{comanda_id}")
def delete_comanda(comanda_id: str, db: Session = Depends(get_db)):
    comanda = db.query(Comanda).filter(Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda nu există")
    
    # Ștergem și piesele
    db.query(ComandaPiesa).filter(ComandaPiesa.comanda_id == comanda.id).delete()
    db.delete(comanda)
    db.commit()
    return {"message": "Comandă ștearsă"}

@router.delete("/clients/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Clientul nu există")
    
    # Verificăm dacă are comenzi
    comenzi = db.query(Comanda).filter(Comanda.client_id == client.id).count()
    if comenzi > 0:
        raise HTTPException(status_code=400, detail="Clientul are comenzi. Nu poate fi șters.")
    
    db.delete(client)
    db.commit()
    return {"message": "Client șters"}
