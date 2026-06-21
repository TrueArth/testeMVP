SELECT id, nome, pontuacao, criado_em, atualizado_em
FROM sintomas
WHERE deleted_at IS NULL
ORDER BY nome ASC;
