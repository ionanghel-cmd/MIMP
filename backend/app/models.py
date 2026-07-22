from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import date

class OrderStatus(str, enum.Enum):
    CERERE = "Cerere"
    OFERTA = "Oferta trimisa"
    CONFIRMATA = "Confirmata"
    COMANDATA = "Comandata la furnizor"
    TRANSPORT = "In transport"
    AJUNSA = "Ajunsa"
    LIVRATA = "Livrată"
    FINALIZATA = "Finalizata"
    ANULATA = "Anulata"

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    nume = Column(String, index=True)
    telefon = Column(String, unique=True, index=True)
    email = Column(String)
    oras = Column(String)
    tara = Column(String, default="Romania")
    tip = Column(String, default="persoana")
    discount = Column(Float, default=0.0)
    limita_credit = Column(Float, default=0.0)
    observatii = Column(String)

class Produs(Base):
    __tablename__ = "produse"
    id = Column(Integer, primary_key=True, index=True)
    cod_oem = Column(String, unique=True, index=True)
    cod_furnizor = Column(String)
    marca = Column(String)
    model = Column(String)
    an = Column(String)
    categorie = Column(String)
    cost_furnizor = Column(Float)
    cost_transport_unit = Column(Float, default=0.0)
    pret_vanzare = Column(Float)
    profit = Column(Float)

class Comanda(Base):
    __tablename__ = "comenzi"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, default=date.today)
    client_id = Column(Integer, ForeignKey("clients.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.CERERE)
    observatii = Column(String)
    total_profit = Column(Float, default=0.0)

    client = relationship("Client")