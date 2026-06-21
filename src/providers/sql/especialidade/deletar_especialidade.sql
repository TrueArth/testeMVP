UPDATE especialidades
SET deleted_at = CURRENT_TIMESTAMP, atualizado_em = CURRENT_TIMESTAMP
WHERE id = #id AND deleted_at IS NULL
RETURNING id, nome, deleted_at;
