INSERT INTO regras_gravidade (sintoma_id, especialidade_id, pontuacao, criado_em, atualizado_em)
VALUES (#sintoma_id, #especialidade_id, #pontuacao, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT(sintoma_id, especialidade_id) DO UPDATE SET
    pontuacao = EXCLUDED.pontuacao,
    deleted_at = NULL,
    atualizado_em = CURRENT_TIMESTAMP
RETURNING sintoma_id, especialidade_id, pontuacao, criado_em, atualizado_em;
