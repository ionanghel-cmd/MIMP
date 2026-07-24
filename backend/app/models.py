from sqlalchemy import Column, String, Float, Date, ForeignKey, Integer, Enum as SQLEnum, Text
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
    LIVRATA = "Livrata"
    FINALIZATA = "Finalizata"
    ANULATA = "Anulata"

class Client(Base):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nume = Column(String, nullable=False)
    telefon = Column(String, unique=True)
    email = Column(String)
    oras = Column(String)
    tip = Column(String, default="persoana")

class Comanda(Base):
    __tablename__ = "comenzi"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numar = Column(Integer, autoincrement=True)
    data = Column(Date, default=date.today)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.CERERE)
    observatii = Column(Text)
    cost_transport_total = Column(Float, default=0.0)
    total_vanzare = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)

    client = relationship("Client", back_populates="comenzi")
    piese = relationship("ComandaPiesa", back_populates="comanda", cascade="all, delete-orphan")

class ComandaPiesa(Base):
    __tablename__ = "comanda_piese"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comanda_id = Column(UUID(as_uuid=True), ForeignKey("comenzi.id"))
    cod_oem = Column(String)
    denumire = Column(String)
    cantitate = Column(Integer, default=1)
    pret_cumparare = Column(Float)
    cost_livrare = Column(Float, default=0.0)
    pret_vanzare = Column(Float)
    profit = Column(Float, default=0.0)

    comanda = relationship("Comanda", back_populates="piese")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="operator")
