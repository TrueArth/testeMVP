UPDATE interconsulta_pedidos
SET 
    status = #status, 
    marcado_por = #marcado_por, 
    data_consulta = #data_consulta,
    atualizado_em = CURRENT_TIMESTAMP
WHERE id = #id AND deleted_at IS NULL
RETURNING id, status, marcado_por, data_consulta, atualizado_em;
