from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..resources.database import Base

class Sintoma(Base):
    """
    Representa um sintoma na base de dados local.
    """
    __tablename__ = "sintomas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    pontuacao = Column(Integer, nullable=False, default=1)
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
