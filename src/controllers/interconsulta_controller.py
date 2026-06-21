from fastapi import HTTPException, BackgroundTasks
from typing import List, Dict, Any
from cryptography.fernet import InvalidToken
from src.services.queue_optimizer_service import QueueOptimizerService

from src.providers.interfaces.interconsulta_provider_interface import InterconsultaProviderInterface
from src.services.risk_engine_service import RiskEngineService
from src.helpers.messaging_helper import MessageBroker
from src.workers.central_marcacao_worker import enviar_para_central_aghu

def resolver_nome_por_cns(cns: str) -> str:
    import os
    import csv
    cns_to_nome = {
        "111111111111111": "CARLA DIAS (CSV)",
        "222222222222222": "BRUNO LIMA (CSV)",
        "333333333333333": "FERNANDA COSTA (CSV)",
        "444444444444444": "LUCAS ALMEIDA (CSV)",
        "555555555555555": "MARIA DA SILVA",
        "666666666666666": "JOÃO DOS SANTOS",
        "777777777777777": "ANA OLIVEIRA",
        "888888888888888": "ROBERTO SOUZA"
    }
    try:
        csv_path = "data/pacientes.csv"
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cns_val = row.get("cns")
                    nome_val = row.get("nome")
                    if cns_val and nome_val:
                        cns_to_nome[cns_val.strip()] = nome_val.strip()
    except Exception:
        pass
    return cns_to_nome.get(cns, "Desconhecido")

def _format_error(exc: Exception) -> str:
    """Mensagem legível para HTTP detail (ex.: InvalidToken tem str vazio)."""
    if isinstance(exc, InvalidToken):
        return (
            "Não foi possível descriptografar o CNS. "
            "A AES_SECRET_KEY do .env mudou desde que os pedidos foram gravados. "
            "Apague os registros antigos em interconsulta_pedidos ou restaure a chave anterior."
        )
    return str(exc) or f"{type(exc).__name__}"


class InterconsultaController:
    """
    Controlador responsável por orquestrar a criação de interconsultas.
    Aplica o motor de regras, delega a persistência e enfileira no Message Broker.
    """
    
    @staticmethod
    async def solicitar_interconsulta(
        payload: dict, 
        provider: InterconsultaProviderInterface,
        background_tasks: BackgroundTasks,
        catalogo_provider: Any = None
    ) -> dict:
        """
        Recebe o payload da API, processa e persiste a interconsulta.
        """
        sintomas = payload.get("sintomas_json", [])
        
        # 1. Processamento pelo Motor de Regras (Carrega catálogos dinâmicos se o provider de catálogo for passado)
        sintomas_db = None
        regras_db = None
        if catalogo_provider is not None:
            try:
                sintomas_db = await catalogo_provider.listar_sintomas()
                regras_db = await catalogo_provider.listar_regras_gravidade()
            except Exception:
                pass
                
        gravidade = RiskEngineService.calcular_gravidade(
            sintomas, 
            payload.get("especialidade_id"),
            sintomas_db=sintomas_db,
            regras_db=regras_db
        )
        payload["gravidade"] = gravidade
        payload["status"] = "PENDENTE"
        
        # 2. Persistência de Dados via Provider (Criptografia e Soft Delete aplicados no provider)
        try:
            pedido_criado = await provider.inserir_pedido(payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar o pedido: {_format_error(e)}")
            
        # Resolve o nome do paciente
        pedido_criado["paciente_nome"] = resolver_nome_por_cns(pedido_criado.get("paciente_cns"))
        return pedido_criado

    @staticmethod
    async def listar_pedidos(provider: InterconsultaProviderInterface, current_user: dict) -> List[Dict[str, Any]]:
        """
        Retorna as interconsultas ativas.
        """
        try:
            pedidos_estaticos = await provider.listar_pedidos_ativos()
            fila_inteligente = QueueOptimizerService.reordenar_fila_dinamica(pedidos_estaticos)
            
            # Resolve os nomes de cada paciente
            for p in fila_inteligente:
                p["paciente_nome"] = resolver_nome_por_cns(p.get("paciente_cns"))
                
            # Se o usuário não for administrador, remove da visão da central 1 dia após a consulta
            if current_user.get("role") != "admin":
                from datetime import datetime, timezone, timedelta
                hoje = datetime.now(timezone.utc)
                filtrados = []
                for p in fila_inteligente:
                    data_cons = p.get("data_consulta")
                    if p.get("status") == "AGENDADO" and data_cons:
                        if isinstance(data_cons, str):
                            try:
                                data_cons = datetime.fromisoformat(data_cons.replace("Z", "+00:00"))
                            except ValueError:
                                data_cons = None
                        if data_cons:
                            if data_cons.tzinfo is None:
                                data_cons = data_cons.replace(tzinfo=timezone.utc)
                            if hoje > data_cons + timedelta(days=1):
                                continue # Oculta do regulador
                    filtrados.append(p)
                fila_inteligente = filtrados

            # Trilha de Auditoria (LGPD)
            username = current_user.get("username") or current_user.get("name") or "Desconhecido"
            import logging
            logger = logging.getLogger("audit")
            logger.warning(
                f"AUDITORIA: Usuario '{username}' visualizou os dados sensiveis (CNS) de {len(fila_inteligente)} pedido(s) de interconsulta."
            )
            return fila_inteligente
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {_format_error(e)}")
            
    @staticmethod
    async def cancelar_pedido(pedido_id: int, provider: InterconsultaProviderInterface) -> dict:
        """
        Aplica o Soft Delete no pedido.
        """
        sucesso = await provider.inativar_pedido(pedido_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Pedido não encontrado ou já cancelado.")
        return {"message": "Pedido cancelado com sucesso."}

    @staticmethod
    async def atualizar_status(pedido_id: int, status: str, provider: InterconsultaProviderInterface, marcado_por: str = None, data_consulta: Any = None) -> dict:
        """
        Atualiza o status de um pedido de interconsulta.
        """
        if status == "AGENDADO":
            if not data_consulta:
                raise HTTPException(status_code=400, detail="Data da consulta é obrigatória para agendamento.")
            
            from datetime import datetime, timezone, timedelta
            val_date = data_consulta
            if isinstance(val_date, str):
                try:
                    val_date = datetime.fromisoformat(val_date.replace("Z", "+00:00"))
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de data inválido. Use o formato ISO.")
            
            if val_date:
                if val_date.tzinfo is None:
                    val_date = val_date.replace(tzinfo=timezone.utc)
                hoje = datetime.now(timezone.utc)
                # Permite uma margem de tolerância de 1 minuto para evitar falsos positivos
                if val_date < hoje - timedelta(minutes=1):
                    raise HTTPException(
                        status_code=400,
                        detail="Não é possível agendar uma consulta para uma data/horário no passado."
                    )

        try:
            sucesso = await provider.atualizar_status_pedido(pedido_id, status, marcado_por=marcado_por, data_consulta=data_consulta)
            if not sucesso:
                raise HTTPException(status_code=404, detail="Pedido não encontrado ou inativo.")
            return {"message": "Status atualizado com sucesso.", "pedido_id": pedido_id, "novo_status": status}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar status: {_format_error(e)}")

    @staticmethod
    async def reprocessar_envio(
        pedido_id: int, 
        provider: InterconsultaProviderInterface, 
        background_tasks: BackgroundTasks
    ) -> dict:
        """
        Força o re-enfileiramento de um pedido com status de ERRO.
        """
        try:
            # 1. Busca os pedidos ativos para encontrar o correspondente
            pedidos = await provider.listar_pedidos_ativos()
            pedido = next((p for p in pedidos if p["id"] == pedido_id), None)
            
            if not pedido:
                raise HTTPException(status_code=404, detail="Pedido não encontrado ou inativo.")
                
            if pedido.get("status") not in ["ERRO", "PENDENTE", "ENFILEIRADO"]:
                raise HTTPException(status_code=400, detail=f"Apenas pedidos com falha ou pendentes podem ser re-enviados. Status atual: {pedido.get('status')}")
                
            # 2. Atualiza o status para ENFILEIRADO
            await provider.atualizar_status_pedido(pedido_id, "ENFILEIRADO")
            pedido["status"] = "ENFILEIRADO"
            
            # 3. Dispara o worker assíncrono
            MessageBroker.dispatch(background_tasks, enviar_para_central_aghu, pedido)
            
            return {"message": "Re-envio disparado com sucesso.", "pedido_id": pedido_id}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao reprocessar envio: {_format_error(e)}")
