SELECT id, nome, criado_em, atualizado_em
FROM especialidades
WHERE deleted_at IS NULL
ORDER BY nome ASC;
