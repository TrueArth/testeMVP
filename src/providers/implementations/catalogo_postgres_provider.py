import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from ..interfaces.catalogo_provider_interface import CatalogoProviderInterface
from src.helpers.sql_helper import create_query, read_sql_file

def _get_sql_path(module: str, filename: str) -> str:
    """Retorna o caminho absoluto para um arquivo SQL de catálogo."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', '..', 'providers', 'sql', module, filename)

class CatalogoPostgresProvider(CatalogoProviderInterface):
    """
    Provedor de dados para especialidades, sintomas e regras usando SQL nativo.
    """

    def __init__(self, session: AsyncSession, dialect: str = "postgresql"):
        self.session = session
        self._dialect = dialect.lower()

    # --- Especialidades ---

    async def inserir_especialidade(self, nome: str) -> dict:
        params = {"nome": nome}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("especialidade", "inserir_especialidade.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            new_id = result.lastrowid
            
            res = await self.session.execute(
                text("SELECT id, nome, criado_em, atualizado_em FROM especialidades WHERE id = :id"),
                {"id": new_id}
            )
            row = res.mappings().first()
            return dict(row) if row else {}
        else:
            sql_template = read_sql_file(_get_sql_path("especialidade", "inserir_especialidade.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return dict(row) if row else {}

    async def listar_especialidades(self) -> List[Dict[str, Any]]:
        sql_template = read_sql_file(_get_sql_path("especialidade", "listar_especialidades.sql"))
        result = await self.session.execute(text(sql_template))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    async def inativar_especialidade(self, especialidade_id: int) -> bool:
        params = {"id": especialidade_id}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("especialidade", "deletar_especialidade.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            return result.rowcount > 0
        else:
            sql_template = read_sql_file(_get_sql_path("especialidade", "deletar_especialidade.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return row is not None

    # --- Sintomas ---

    async def inserir_sintoma(self, nome: str, pontuacao: int) -> dict:
        params = {"nome": nome, "pontuacao": pontuacao}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("sintoma", "inserir_sintoma.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            new_id = result.lastrowid
            
            res = await self.session.execute(
                text("SELECT id, nome, pontuacao, criado_em, atualizado_em FROM sintomas WHERE id = :id"),
                {"id": new_id}
            )
            row = res.mappings().first()
            return dict(row) if row else {}
        else:
            sql_template = read_sql_file(_get_sql_path("sintoma", "inserir_sintoma.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return dict(row) if row else {}

    async def listar_sintomas(self) -> List[Dict[str, Any]]:
        sql_template = read_sql_file(_get_sql_path("sintoma", "listar_sintomas.sql"))
        result = await self.session.execute(text(sql_template))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    async def listar_sintomas_por_especialidade(self, especialidade_id: int) -> List[Dict[str, Any]]:
        params = {"especialidade_id": especialidade_id}
        sql_template = read_sql_file(_get_sql_path("sintoma", "listar_sintomas_por_especialidade.sql"))
        query_str = create_query(sql_template, params)
        result = await self.session.execute(text(query_str))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    async def inativar_sintoma(self, sintoma_id: int) -> bool:
        params = {"id": sintoma_id}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("sintoma", "deletar_sintoma.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            return result.rowcount > 0
        else:
            sql_template = read_sql_file(_get_sql_path("sintoma", "deletar_sintoma.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return row is not None

    # --- Regras de Gravidade ---

    async def inserir_regra_gravidade(self, sintoma_id: int, especialidade_id: int, pontuacao: int) -> dict:
        params = {"sintoma_id": sintoma_id, "especialidade_id": especialidade_id, "pontuacao": pontuacao}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("regra_gravidade", "inserir_regra.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            await self.session.execute(text(query_str))
            await self.session.commit()
            
            res = await self.session.execute(
                text("SELECT sintoma_id, especialidade_id, pontuacao, criado_em, atualizado_em FROM regras_gravidade WHERE sintoma_id = :s_id AND especialidade_id = :e_id"),
                {"s_id": sintoma_id, "e_id": especialidade_id}
            )
            row = res.mappings().first()
            return dict(row) if row else {}
        else:
            sql_template = read_sql_file(_get_sql_path("regra_gravidade", "inserir_regra.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return dict(row) if row else {}

    async def listar_regras_gravidade(self) -> List[Dict[str, Any]]:
        sql_template = read_sql_file(_get_sql_path("regra_gravidade", "listar_regras.sql"))
        result = await self.session.execute(text(sql_template))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    async def inativar_regra_gravidade(self, sintoma_id: int, especialidade_id: int) -> bool:
        params = {"sintoma_id": sintoma_id, "especialidade_id": especialidade_id}
        if self._dialect == "sqlite":
            sql_template = read_sql_file(_get_sql_path("regra_gravidade", "deletar_regra.sql"))
            sql_clean = sql_template.split("RETURNING")[0].rstrip().rstrip(";")
            query_str = create_query(sql_clean, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            return result.rowcount > 0
        else:
            sql_template = read_sql_file(_get_sql_path("regra_gravidade", "deletar_regra.sql"))
            query_str = create_query(sql_template, params)
            result = await self.session.execute(text(query_str))
            await self.session.commit()
            row = result.mappings().first()
            return row is not None
