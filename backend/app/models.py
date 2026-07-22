from sqlalchemy import Column, String, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
import enum
from datetime import date

Base = declarative_base()

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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cod_oem = Column(String, unique=True, index=True)
    marca = Column(String)
    cost_furnizor = Column(Float)
    pret_vanzare = Column(Float)
    profit = Column(Float)

class Comanda(Base):
    __tablename__ = "comenzi"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    data = Column(Date, default=date.today)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.CERERE)
    observatii = Column(String)
    total_profit = Column(Float, default=0.0)

    client = relationship("Client")
