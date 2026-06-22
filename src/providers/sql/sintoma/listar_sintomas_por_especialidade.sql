SELECT s.id, s.nome, s.pontuacao, s.criado_em, s.atualizado_em
FROM sintomas s
INNER JOIN regras_gravidade r ON s.id = r.sintoma_id
WHERE r.especialidade_id = #especialidade_id AND s.deleted_at IS NULL AND r.deleted_at IS NULL
ORDER BY s.nome ASC;
