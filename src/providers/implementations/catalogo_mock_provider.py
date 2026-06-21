import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any

from ..interfaces.catalogo_provider_interface import CatalogoProviderInterface

class CatalogoMockProvider(CatalogoProviderInterface):
    """
    Mock data provider for Specialties, Symptoms, and Rules.
    Persists data in local JSON files.
    """

    def __init__(
        self,
        esps_path: str = "data/especialidades.json",
        sints_path: str = "data/sintomas.json",
        rules_path: str = "data/regras_gravidade.json"
    ):
        self.esps_path = esps_path
        self.sints_path = sints_path
        self.rules_path = rules_path
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        # 1. Specialties
        os.makedirs(os.path.dirname(self.esps_path), exist_ok=True)
        if not os.path.exists(self.esps_path) or self._load_file(self.esps_path) == []:
            mock_esps = [
                {"id": 1, "nome": "Cardiologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 2, "nome": "Clínica Médica", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 3, "nome": "Dermatologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 4, "nome": "Endocrinologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 5, "nome": "Gastroenterologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 6, "nome": "Geriatria", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 7, "nome": "Hematologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 8, "nome": "Infectologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 9, "nome": "Medicina de Família e Comunidade", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 10, "nome": "Medicina do Trabalho", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 11, "nome": "Nefrologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 12, "nome": "Neurologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 13, "nome": "Oncologia (Alta Complexidade - CACON)", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 14, "nome": "Pediatria", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 15, "nome": "Pneumologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 16, "nome": "Psiquiatria", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 17, "nome": "Reumatologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 18, "nome": "Urologia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 19, "nome": "Ginecologia e Obstetrícia", "criado_em": None, "atualizado_em": None, "deleted_at": None},
            ]
            self._save_file(self.esps_path, mock_esps)

        # 2. Symptoms
        os.makedirs(os.path.dirname(self.sints_path), exist_ok=True)
        sints_data = self._load_file(self.sints_path) if os.path.exists(self.sints_path) else []
        has_old_sints = any("gravidade_padrao" in item for item in sints_data)
        if not os.path.exists(self.sints_path) or sints_data == [] or has_old_sints:
            mock_sints = [
                {"id": 1, "nome": "Cegueira / Perda súbita de visão", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 2, "nome": "Infarto / Dor torácica súbita", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 3, "nome": "AVC / Perda de força unilateral", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 4, "nome": "Dor torácica intensa", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 5, "nome": "Febre alta", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 6, "nome": "Fratura", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 7, "nome": "Ideação suicida ativa", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 8, "nome": "Hematúria macroscópica", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 9, "nome": "Nódulo tireoidiano palpável", "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 10, "nome": "Dispneia aguda", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 11, "nome": "Dor abdominal intensa", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 12, "nome": "Convulsão", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 13, "nome": "Erupção cutânea com febre", "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"id": 14, "nome": "Confusão mental aguda", "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            ]
            self._save_file(self.sints_path, mock_sints)

        # 3. Rules (Overrides)
        os.makedirs(os.path.dirname(self.rules_path), exist_ok=True)
        rules_data = self._load_file(self.rules_path) if os.path.exists(self.rules_path) else []
        has_old_rules = any("gravidade" in item for item in rules_data)
        if not os.path.exists(self.rules_path) or rules_data == [] or has_old_rules:
            mock_rules = [
                {"sintoma_id": 4, "especialidade_id": 1, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 10, "especialidade_id": 1, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 13, "especialidade_id": 3, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 9, "especialidade_id": 4, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 11, "especialidade_id": 5, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 14, "especialidade_id": 6, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 5, "especialidade_id": 8, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 13, "especialidade_id": 8, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 8, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 12, "especialidade_id": 12, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 14, "especialidade_id": 12, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 9, "especialidade_id": 13, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 5, "especialidade_id": 14, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 12, "especialidade_id": 14, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 10, "especialidade_id": 15, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 7, "especialidade_id": 16, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 6, "especialidade_id": 17, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
                {"sintoma_id": 8, "especialidade_id": 18, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            ]
            self._save_file(self.rules_path, mock_rules)

    def _load_file(self, path: str) -> List[Dict[str, Any]]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_file(self, path: str, data: List[Dict[str, Any]]):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # --- Specialties ---

    async def inserir_especialidade(self, nome: str) -> dict:
        data = self._load_file(self.esps_path)
        next_id = max([item.get("id", 0) for item in data]) + 1 if data else 1
        now = datetime.now(timezone.utc).isoformat()
        
        record = {
            "id": next_id,
            "nome": nome,
            "criado_em": now,
            "atualizado_em": now,
            "deleted_at": None
        }
        data.append(record)
        self._save_file(self.esps_path, data)
        return record

    async def listar_especialidades(self) -> List[Dict[str, Any]]:
        data = self._load_file(self.esps_path)
        return [r for r in data if r.get("deleted_at") is None]

    async def inativar_especialidade(self, especialidade_id: int) -> bool:
        data = self._load_file(self.esps_path)
        found = False
        now = datetime.now(timezone.utc).isoformat()
        for r in data:
            if r.get("id") == especialidade_id and r.get("deleted_at") is None:
                r["deleted_at"] = now
                r["atualizado_em"] = now
                found = True
                break
        if found:
            self._save_file(self.esps_path, data)
        return found

    # --- Symptoms ---

    async def inserir_sintoma(self, nome: str, pontuacao: int) -> dict:
        data = self._load_file(self.sints_path)
        next_id = max([item.get("id", 0) for item in data]) + 1 if data else 1
        now = datetime.now(timezone.utc).isoformat()
        
        record = {
            "id": next_id,
            "nome": nome,
            "pontuacao": pontuacao,
            "criado_em": now,
            "atualizado_em": now,
            "deleted_at": None
        }
        data.append(record)
        self._save_file(self.sints_path, data)
        return record

    async def listar_sintomas(self) -> List[Dict[str, Any]]:
        data = self._load_file(self.sints_path)
        return [r for r in data if r.get("deleted_at") is None]

    async def inativar_sintoma(self, sintoma_id: int) -> bool:
        data = self._load_file(self.sints_path)
        found = False
        now = datetime.now(timezone.utc).isoformat()
        for r in data:
            if r.get("id") == sintoma_id and r.get("deleted_at") is None:
                r["deleted_at"] = now
                r["atualizado_em"] = now
                found = True
                break
        if found:
            self._save_file(self.sints_path, data)
        return found

    # --- Rules ---

    async def inserir_regra_gravidade(self, sintoma_id: int, especialidade_id: int, pontuacao: int) -> dict:
        data = self._load_file(self.rules_path)
        now = datetime.now(timezone.utc).isoformat()
        
        # Check existing rule
        found_rule = None
        for r in data:
            if r.get("sintoma_id") == sintoma_id and r.get("especialidade_id") == especialidade_id:
                found_rule = r
                break
                
        if found_rule:
            found_rule["pontuacao"] = pontuacao
            found_rule["deleted_at"] = None
            found_rule["atualizado_em"] = now
            record = found_rule
        else:
            record = {
                "sintoma_id": sintoma_id,
                "especialidade_id": especialidade_id,
                "pontuacao": pontuacao,
                "criado_em": now,
                "atualizado_em": now,
                "deleted_at": None
            }
            data.append(record)
            
        self._save_file(self.rules_path, data)
        return record

    async def listar_regras_gravidade(self) -> List[Dict[str, Any]]:
        data = self._load_file(self.rules_path)
        return [r for r in data if r.get("deleted_at") is None]

    async def inativar_regra_gravidade(self, sintoma_id: int, especialidade_id: int) -> bool:
        data = self._load_file(self.rules_path)
        found = False
        now = datetime.now(timezone.utc).isoformat()
        for r in data:
            if r.get("sintoma_id") == sintoma_id and r.get("especialidade_id") == especialidade_id and r.get("deleted_at") is None:
                r["deleted_at"] = now
                r["atualizado_em"] = now
                found = True
                break
        if found:
            self._save_file(self.rules_path, data)
        return found
