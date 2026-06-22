from abc import ABC, abstractmethod
from typing import List, Dict, Any

class CatalogoProviderInterface(ABC):
    
    @abstractmethod
    async def inserir_especialidade(self, nome: str) -> dict:
        """Insere uma nova especialidade."""
        pass
        
    @abstractmethod
    async def listar_especialidades(self) -> List[Dict[str, Any]]:
        """Lista todas as especialidades ativas."""
        pass
        
    @abstractmethod
    async def inativar_especialidade(self, especialidade_id: int) -> bool:
        """Inativa uma especialidade (Soft Delete)."""
        pass

    @abstractmethod
    async def inserir_sintoma(self, nome: str, pontuacao: int) -> dict:
        """Insere um novo sintoma."""
        pass
        
    @abstractmethod
    async def listar_sintomas(self) -> List[Dict[str, Any]]:
        """Lista todos os sintomas ativos."""
        pass
        
    @abstractmethod
    async def listar_sintomas_por_especialidade(self, especialidade_id: int) -> List[Dict[str, Any]]:
        """Lista sintomas ativos associados a uma especialidade específica."""
        pass
        
    @abstractmethod
    async def inativar_sintoma(self, sintoma_id: int) -> bool:
        """Inativa um sintoma (Soft Delete)."""
        pass

    @abstractmethod
    async def inserir_regra_gravidade(self, sintoma_id: int, especialidade_id: int, pontuacao: int) -> dict:
        """Insere ou atualiza uma regra de pontuação (override) para especialidade/sintoma."""
        pass
        
    @abstractmethod
    async def listar_regras_gravidade(self) -> List[Dict[str, Any]]:
        """Lista todas as regras de gravidade ativas."""
        pass
        
    @abstractmethod
    async def inativar_regra_gravidade(self, sintoma_id: int, especialidade_id: int) -> bool:
        """Inativa/remove uma regra de gravidade (Soft Delete)."""
        pass
