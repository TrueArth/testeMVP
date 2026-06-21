from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..resources.database import Base

class Especialidade(Base):
    """
    Representa uma especialidade médica na base de dados local.
    """
    __tablename__ = "especialidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
