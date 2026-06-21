from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..resources.database import Base

class RegraGravidade(Base):
    """
    Representa uma regra de gravidade (override) para um sintoma em uma especialidade.
    """
    __tablename__ = "regras_gravidade"

    sintoma_id = Column(Integer, primary_key=True, nullable=False)
    especialidade_id = Column(Integer, primary_key=True, nullable=False)
    pontuacao = Column(Integer, nullable=False, default=1)
    
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
