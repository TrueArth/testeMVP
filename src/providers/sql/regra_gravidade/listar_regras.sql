SELECT sintoma_id, especialidade_id, pontuacao, criado_em, atualizado_em
FROM regras_gravidade
WHERE deleted_at IS NULL;
