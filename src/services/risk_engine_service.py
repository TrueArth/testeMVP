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
        15: 10, # Doença Renal Crônica estágio V
        16: 10, # Síndrome Nefrótica grave
        17: 10, # Síndrome Nefrítica ou Glomerulonefrite rapidamente progressiva
        18: 10, # Hipertensão arterial acelerada ou maligna
        19: 10, # Injúria renal aguda
        20: 10, # Alterações em sumário de urina com Injúria renal aguda
        21: 5,  # Doença Renal Crônica estágio IIIa a IV
        22: 5,  # Sinais/sintomas e alterações laboratoriais de DMO-DRC
        23: 5,  # DRC/dialítico com osteoporose e/ou fraturas
        24: 5,  # DRC/dialítico com hiperparatireoidismo secundário grave
        25: 5,  # Transplantado renal com osteoporose ou hiperparatireoidismo persistente
        26: 5,  # DRC de etiologia indeterminada com suspeita de causa genética/rara
        27: 5,  # Investigação de síndrome nefrótica ou nefrítica familiar
        28: 5,  # Distúrbio hidroeletrolítico de difícil diagnóstico e manejo
        29: 5,  # Investigação de nefrocalcinose sem causa definida
        30: 5,  # Síndrome Nefrótica leve a moderada
        31: 2,  # Hematúria isolada
        32: 2,  # Proteinúria subnefrótica isolada
        33: 2,  # Doença Renal Crônica estágio I ou II
        34: 2,  # Infecções urinárias complicadas
    }
    
    # Overrides específicos de especialidade: (sintoma_id, especialidade_id) -> pontuacao
    SPECIALTY_OVERRIDES_SCORES = {
        # Cardiologia (ID 1)
        (4, 1): 10,  # Dor torácica intensa -> 10 (VERMELHO)
        (10, 1): 10, # Dispneia aguda -> 10 (VERMELHO)
        (2, 1): 10,  # Infarto / Dor torácica súbita -> 10 (VERMELHO)
        # Clínica Médica (ID 2)
        (5, 2): 5,   # Febre alta -> 5 (AMARELO)
        (12, 2): 5,  # Convulsão -> 5 (AMARELO)
        (14, 2): 1,  # Confusão mental aguda -> 1 (VERDE)
        # Dermatologia (ID 3)
        (13, 3): 5,  # Erupção cutânea com febre -> 5 (AMARELO)
        (9, 3): 1,   # Nódulo tireoidiano palpável -> 1 (VERDE)
        # Endocrinologia (ID 4)
        (9, 4): 5,   # Nódulo tireoidiano palpável -> 5 (AMARELO)
        (5, 4): 5,   # Febre alta -> 5 (AMARELO)
        # Gastroenterologia (ID 5)
        (11, 5): 10, # Dor abdominal intensa -> 10 (VERMELHO)
        (10, 5): 5,  # Dispneia aguda -> 5 (AMARELO)
        # Geriatria (ID 6)
        (14, 6): 5,  # Confusão mental aguda -> 5 (AMARELO)
        (7, 6): 5,   # Ideação suicida ativa -> 5 (AMARELO)
        # Hematologia (ID 7)
        (8, 7): 5,   # Hematúria macroscópica -> 5 (AMARELO)
        (5, 7): 5,   # Febre alta -> 5 (AMARELO)
        # Infectologia (ID 8)
        (5, 8): 5,   # Febre alta -> 5 (AMARELO)
        (13, 8): 5,  # Erupção cutânea com febre -> 5 (AMARELO)
        # Medicina de Família e Comunidade (ID 9)
        (1, 9): 10,  # Cegueira / Perda súbita de visão -> 10 (VERMELHO)
        (4, 9): 5,   # Dor torácica intensa -> 5 (AMARELO)
        (5, 9): 5,   # Febre alta -> 5 (AMARELO)
        (6, 9): 5,   # Fratura -> 5 (AMARELO)
        # Medicina do Trabalho (ID 10)
        (4, 10): 5,  # Dor torácica intensa -> 5 (AMARELO)
        (14, 10): 1, # Confusão mental aguda -> 1 (VERDE)
        # Nefrologia (ID 11)
        (8, 11): 10,  # Hematúria macroscópica -> 10 (VERMELHO)
        (15, 11): 10, # Doença Renal Crônica estágio V -> 10 (VERMELHO)
        (16, 11): 10, # Síndrome Nefrótica grave -> 10 (VERMELHO)
        (17, 11): 10, # Síndrome Nefrítica -> 10 (VERMELHO)
        (18, 11): 10, # Hipertensão acelerada/maligna -> 10 (VERMELHO)
        (19, 11): 10, # Injúria renal aguda -> 10 (VERMELHO)
        (20, 11): 10, # Alterações em sumário de urina com Injúria renal aguda -> 10 (VERMELHO)
        (21, 11): 5,  # DRC estágio IIIa a IV -> 5 (AMARELO)
        (22, 11): 5,  # DMO-DRC -> 5 (AMARELO)
        (23, 11): 5,  # DRC/dialítico com osteoporose/fraturas -> 5 (AMARELO)
        (24, 11): 5,  # DRC/dialítico com hiperparatireoidismo grave -> 5 (AMARELO)
        (25, 11): 5,  # Transplantado renal com osteoporose/hiperparatireoidismo -> 5 (AMARELO)
        (26, 11): 5,  # DRC de etiologia indeterminada (genética) -> 5 (AMARELO)
        (27, 11): 5,  # Síndrome nefrótica/nefrítica familiar -> 5 (AMARELO)
        (28, 11): 5,  # Distúrbios hidroeletrolíticos -> 5 (AMARELO)
        (29, 11): 5,  # Nefrocalcinose -> 5 (AMARELO)
        (30, 11): 5,  # Síndrome Nefrótica leve a moderada -> 5 (AMARELO)
        (31, 11): 2,  # Hematúria isolada -> 2 (VERDE)
        (32, 11): 2,  # Proteinúria subnefrótica -> 2 (VERDE)
        (33, 11): 2,  # DRC estágio I ou II -> 2 (VERDE)
        (34, 11): 2,  # Infecções urinárias complicadas -> 2 (VERDE)
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
        # Ginecologia e Obstetrícia (ID 19)
        (11, 19): 5,  # Dor abdominal intensa -> 5 (AMARELO)
        (5, 19): 5,   # Febre alta -> 5 (AMARELO)
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
