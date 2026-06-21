INSERT INTO sintomas (nome, pontuacao, criado_em, atualizado_em)
VALUES (#nome, #pontuacao, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
RETURNING id, nome, pontuacao, criado_em, atualizado_em;
