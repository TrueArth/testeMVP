UPDATE regras_gravidade
SET deleted_at = CURRENT_TIMESTAMP, atualizado_em = CURRENT_TIMESTAMP
WHERE sintoma_id = #sintoma_id AND especialidade_id = #especialidade_id AND deleted_at IS NULL
RETURNING sintoma_id, especialidade_id, deleted_at;
