class RiskEngineService:
    """
    Serviço puro responsável por calcular a gravidade clínica (Risco)
    baseado no acúmulo de pontuação dos sintomas e especialidade de destino.
    """
    
    # Pontuação padrão dos sintomas (VERMELHO = 10, AMARELO = 5, VERDE = 1)
    SINTOMAS_PADRAO_SCORES = {
        1: 10,  # Cegueira / Perda súbita de visão
        2: 10,  # Infarto / Dor torácica súbita
        3: 10,  # AVC / Perda de força unilateral
        4: 5,   # Dor torácica intensa
        5: 5,   # Febre alta
        6: 5,   # Fratura
        7: 5,   # Ideação suicida ativa
        8: 5,   # Hematúria macroscópica
        9: 1,   # Nódulo tireoidiano palpável
        10: 5,  # Dispneia aguda
        11: 5,  # Dor abdominal intensa
        12: 5,  # Convulsão
        13: 1,  # Erupção cutânea com febre
        14: 1,  # Confusão mental aguda
    }
    
    # Overrides específicos de especialidade: (sintoma_id, especialidade_id) -> pontuacao
    SPECIALTY_OVERRIDES_SCORES = {
        # Cardiologia (ID 1)
        (4, 1): 10,  # Dor torácica intensa -> 10 (VERMELHO)
        (10, 1): 10, # Dispneia aguda -> 10 (VERMELHO)
        # Dermatologia (ID 3)
        (13, 3): 5,  # Erupção cutânea com febre -> 5 (AMARELO)
        # Endocrinologia (ID 4)
        (9, 4): 5,   # Nódulo tireoidiano palpável -> 5 (AMARELO)
        # Gastroenterologia (ID 5)
        (11, 5): 10, # Dor abdominal intensa -> 10 (VERMELHO)
        # Geriatria (ID 6)
        (14, 6): 5,  # Confusão mental aguda -> 5 (AMARELO)
        # Infectologia (ID 8)
        (5, 8): 5,   # Febre alta -> 5 (AMARELO)
        (13, 8): 5,  # Erupção cutânea com febre -> 5 (AMARELO)
        # Nefrologia (ID 11)
        (8, 11): 10, # Hematúria macroscópica -> 10 (VERMELHO)
        # Neurologia (ID 12)
        (12, 12): 10, # Convulsão -> 10 (VERMELHO)
        (14, 12): 5,  # Confusão mental aguda -> 5 (AMARELO)
        # Oncologia (ID 13)
        (9, 13): 5,   # Nódulo tireoidiano -> 5 (AMARELO)
        # Pediatria (ID 14)
        (5, 14): 5,   # Febre alta -> 5 (AMARELO)
        (12, 14): 10, # Convulsão -> 10 (VERMELHO)
        # Pneumologia (ID 15)
        (10, 15): 10, # Dispneia aguda -> 10 (VERMELHO)
        # Psiquiatria (ID 16)
        (7, 16): 10,  # Ideação suicida ativa -> 10 (VERMELHO)
        # Reumatologia (ID 17)
        (6, 17): 5,   # Fratura -> 5 (AMARELO)
        # Urologia (ID 18)
        (8, 18): 10,  # Hematúria macroscópica -> 10 (VERMELHO)
    }

    @staticmethod
    def calcular_gravidade(
        sintomas: list,
        especialidade_id: int = None,
        sintomas_db: list = None,
        regras_db: list = None
    ) -> str:
        """
        Recebe uma lista de dicionários de sintomas (ex: [{"id": 1, "nome": "Cegueira"}])
        e a especialidade desejada, e retorna a cor da gravidade (VERMELHO, AMARELO, VERDE)
        baseada na soma das pontuações acumuladas.
        """
        if not sintomas:
            return "VERDE"
            
        sintomas_ids = [s.get("id") for s in sintomas if isinstance(s, dict) and "id" in s]
        
        # Constrói mapas a partir do banco de dados (se passados e não vazios)
        if sintomas_db and regras_db is not None:
            sintomas_scores = {s["id"]: int(s.get("pontuacao", 1)) for s in sintomas_db}
            overrides = {(r["sintoma_id"], r["especialidade_id"]): int(r.get("pontuacao", 1)) for r in regras_db}
        else:
            sintomas_scores = RiskEngineService.SINTOMAS_PADRAO_SCORES
            overrides = RiskEngineService.SPECIALTY_OVERRIDES_SCORES
            
        total_score = 0
        
        for sid in sintomas_ids:
            score = 1  # Fallback default
            if especialidade_id is not None and (sid, especialidade_id) in overrides:
                score = overrides[(sid, especialidade_id)]
            else:
                score = sintomas_scores.get(sid, 1)
            total_score += score
            
        # Classificação baseada no total acumulado
        if total_score >= 10:
            return "VERMELHO"
        elif total_score >= 5:
            return "AMARELO"
        else:
            return "VERDE"
