from typing import List, Dict, Any
from fastapi import HTTPException, status
from src.providers.interfaces.catalogo_provider_interface import CatalogoProviderInterface

class CatalogoController:
    """
    Controlador responsável pelas regras de negócio e CRUD de
    Especialidades, Sintomas e Regras de Gravidade.
    """

    # --- Especialidades ---

    @staticmethod
    async def criar_especialidade(nome: str, provider: CatalogoProviderInterface) -> dict:
        if not nome or not nome.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome da especialidade inválido.")
        try:
            return await provider.inserir_especialidade(nome.strip())
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar especialidade: {str(e)}")

    @staticmethod
    async def listar_especialidades(provider: CatalogoProviderInterface) -> List[Dict[str, Any]]:
        try:
            return await provider.listar_especialidades()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar especialidades: {str(e)}")

    @staticmethod
    async def inativar_especialidade(especialidade_id: int, provider: CatalogoProviderInterface) -> dict:
        try:
            sucesso = await provider.inativar_especialidade(especialidade_id)
            if not sucesso:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrada ou já inativa.")
            return {"message": "Especialidade inativada com sucesso.", "id": especialidade_id}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao inativar especialidade: {str(e)}")

    # --- Sintomas ---

    @staticmethod
    async def criar_sintoma(nome: str, pontuacao: int, provider: CatalogoProviderInterface) -> dict:
        if not nome or not nome.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome do sintoma inválido.")
        if not isinstance(pontuacao, int) or pontuacao < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pontuação padrão inválida. Deve ser maior ou igual a 1.")
        try:
            return await provider.inserir_sintoma(nome.strip(), pontuacao)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar sintoma: {str(e)}")

    @staticmethod
    async def listar_sintomas(provider: CatalogoProviderInterface) -> List[Dict[str, Any]]:
        try:
            return await provider.listar_sintomas()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar sintomas: {str(e)}")

    @staticmethod
    async def inativar_sintoma(sintoma_id: int, provider: CatalogoProviderInterface) -> dict:
        try:
            sucesso = await provider.inativar_sintoma(sintoma_id)
            if not sucesso:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sintoma não encontrado ou já inativo.")
            return {"message": "Sintoma inativado com sucesso.", "id": sintoma_id}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao inativar sintoma: {str(e)}")

    # --- Regras ---

    @staticmethod
    async def criar_regra_gravidade(sintoma_id: int, especialidade_id: int, pontuacao: int, provider: CatalogoProviderInterface) -> dict:
        if not isinstance(pontuacao, int) or pontuacao < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pontuação de regra inválida. Deve ser maior ou igual a 1.")
        try:
            return await provider.inserir_regra_gravidade(sintoma_id, especialidade_id, pontuacao)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao salvar regra: {str(e)}")

    @staticmethod
    async def listar_regras_gravidade(provider: CatalogoProviderInterface) -> List[Dict[str, Any]]:
        try:
            return await provider.listar_regras_gravidade()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar regras: {str(e)}")

    @staticmethod
    async def inativar_regra_gravidade(sintoma_id: int, especialidade_id: int, provider: CatalogoProviderInterface) -> dict:
        try:
            sucesso = await provider.inativar_regra_gravidade(sintoma_id, especialidade_id)
            if not sucesso:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Regra de gravidade não encontrada.")
            return {"message": "Regra de gravidade removida com sucesso."}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao remover regra: {str(e)}")
