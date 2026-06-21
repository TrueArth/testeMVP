INSERT INTO especialidades (nome, criado_em, atualizado_em)
VALUES (#nome, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING id, nome, criado_em, atualizado_em;
