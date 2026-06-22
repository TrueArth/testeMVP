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
            {"id": 15, "nome": "Doença Renal Crônica estágio V", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 16, "nome": "Síndrome Nefrótica grave (proteinúria > 8g/24h e/ou disfunção renal aguda)", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 17, "nome": "Síndrome Nefrítica ou Glomerulonefrite rapidamente progressiva", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 18, "nome": "Hipertensão arterial acelerada ou maligna", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 19, "nome": "Injúria renal aguda", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 20, "nome": "Alterações em sumário de urina com Injúria renal aguda", "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 21, "nome": "Doença Renal Crônica estágio IIIa a IV", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 22, "nome": "Sinais/sintomas e alterações laboratoriais de DMO-DRC", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 23, "nome": "DRC/dialítico com osteoporose e/ou fraturas", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 24, "nome": "DRC/dialítico com hiperparatireoidismo secundário grave", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 25, "nome": "Transplantado renal com osteoporose ou hiperparatireoidismo persistente", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 26, "nome": "DRC de etiologia indeterminada com suspeita de causa genética/rara", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 27, "nome": "Investigação de síndrome nefrótica ou nefrítica familiar", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 28, "nome": "Distúrbio hidroeletrolítico de difícil diagnóstico e manejo", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 29, "nome": "Investigação de nefrocalcinose sem causa definida", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 30, "nome": "Síndrome Nefrótica leve a moderada (proteinúria < 8g/24h)", "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 31, "nome": "Hematúria isolada", "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 32, "nome": "Proteinúria subnefrótica isolada", "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 33, "nome": "Doença Renal Crônica estágio I ou II", "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"id": 34, "nome": "Infecções urinárias complicadas (repetição e/ou rim único)", "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
        ]
        if not os.path.exists(self.sints_path) or sints_data == [] or has_old_sints:
            sints_data = mock_sints
        else:
            # Merge missing ones
            existing_ids = {item["id"] for item in sints_data}
            for item in mock_sints:
                if item["id"] not in existing_ids:
                    sints_data.append(item)
        self._save_file(self.sints_path, sints_data)

        # 3. Rules (Overrides)
        os.makedirs(os.path.dirname(self.rules_path), exist_ok=True)
        rules_data = self._load_file(self.rules_path) if os.path.exists(self.rules_path) else []
        has_old_rules = any("gravidade" in item for item in rules_data)
        
        mock_rules = [
            {"sintoma_id": 4, "especialidade_id": 1, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 10, "especialidade_id": 1, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 2, "especialidade_id": 1, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Clínica Médica (ID 2)
            {"sintoma_id": 5, "especialidade_id": 2, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 12, "especialidade_id": 2, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 14, "especialidade_id": 2, "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Dermatologia (ID 3)
            {"sintoma_id": 13, "especialidade_id": 3, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 9, "especialidade_id": 3, "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Endocrinologia (ID 4)
            {"sintoma_id": 9, "especialidade_id": 4, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 5, "especialidade_id": 4, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Gastroenterologia (ID 5)
            {"sintoma_id": 11, "especialidade_id": 5, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 10, "especialidade_id": 5, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Geriatria (ID 6)
            {"sintoma_id": 14, "especialidade_id": 6, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 7, "especialidade_id": 6, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Hematologia (ID 7)
            {"sintoma_id": 8, "especialidade_id": 7, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 5, "especialidade_id": 7, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Infectologia (ID 8)
            {"sintoma_id": 5, "especialidade_id": 8, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 13, "especialidade_id": 8, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Medicina de Família e Comunidade (ID 9)
            {"sintoma_id": 1, "especialidade_id": 9, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 4, "especialidade_id": 9, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 5, "especialidade_id": 9, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 6, "especialidade_id": 9, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Medicina do Trabalho (ID 10)
            {"sintoma_id": 4, "especialidade_id": 10, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 14, "especialidade_id": 10, "pontuacao": 1, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Nefrologia (ID 11)
            {"sintoma_id": 8, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Novas regras da Nefrologia (ID 11)
            {"sintoma_id": 15, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 16, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 17, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 18, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 19, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 20, "especialidade_id": 11, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 21, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 22, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 23, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 24, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 25, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 26, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 27, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 28, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 29, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 30, "especialidade_id": 11, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 31, "especialidade_id": 11, "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 32, "especialidade_id": 11, "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 33, "especialidade_id": 11, "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 34, "especialidade_id": 11, "pontuacao": 2, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Neurologia (ID 12)
            {"sintoma_id": 12, "especialidade_id": 12, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 14, "especialidade_id": 12, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Oncologia (ID 13)
            {"sintoma_id": 9, "especialidade_id": 13, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Pediatria (ID 14)
            {"sintoma_id": 5, "especialidade_id": 14, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 12, "especialidade_id": 14, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Pneumologia (ID 15)
            {"sintoma_id": 10, "especialidade_id": 15, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Psiquiatria (ID 16)
            {"sintoma_id": 7, "especialidade_id": 16, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Reumatologia (ID 17)
            {"sintoma_id": 6, "especialidade_id": 17, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Urologia (ID 18)
            {"sintoma_id": 8, "especialidade_id": 18, "pontuacao": 10, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            # Ginecologia e Obstetrícia (ID 19)
            {"sintoma_id": 11, "especialidade_id": 19, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
            {"sintoma_id": 5, "especialidade_id": 19, "pontuacao": 5, "criado_em": None, "atualizado_em": None, "deleted_at": None},
        ]
        if not os.path.exists(self.rules_path) or rules_data == [] or has_old_rules:
            rules_data = mock_rules
        else:
            # Merge missing ones
            existing_rules = {(item["sintoma_id"], item["especialidade_id"]) for item in rules_data}
            for item in mock_rules:
                if (item["sintoma_id"], item["especialidade_id"]) not in existing_rules:
                    rules_data.append(item)
        self._save_file(self.rules_path, rules_data)

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

    async def listar_sintomas_por_especialidade(self, especialidade_id: int) -> List[Dict[str, Any]]:
        rules = await self.listar_regras_gravidade()
        sintomas_ids = {r["sintoma_id"] for r in rules if r["especialidade_id"] == especialidade_id}
        
        sintomas = await self.listar_sintomas()
        return [s for s in sintomas if s["id"] in sintomas_ids]

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
