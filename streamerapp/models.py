from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = 'user'

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()),unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(225), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    stations: Mapped[list["StationService"]] = relationship("StationService", back_populates="owner", cascade="all, delete-orphan")


class StationService(Base):
    __tablename__ = 'stationservice'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()),  unique=True, nullable=False)
    stationservicename: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Foreign key to User
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="stations")
    tanks: Mapped[list["Tank"]] = relationship("Tank", back_populates="station", cascade="all, delete-orphan")


class Tank(Base):
    __tablename__ = 'tank'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    density: Mapped[float] = mapped_column(Float, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updateAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign key to StationService
    station_id: Mapped[str] = mapped_column(String(36), ForeignKey("stationservice.id"), nullable=False)
    
    # Relationships
    station: Mapped["StationService"] = relationship("StationService", back_populates="tanks")