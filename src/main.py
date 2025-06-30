#!/usr/bin/env python3
"""
Servidor MCP para busca de licitações governamentais brasileiras
Integra com PNCP, ComprasNet e outros portais
"""

import asyncio
from typing import Any, Dict, List
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Tool,
    TextContent,
    LoggingLevel
)
import mcp.types as types
from src.api.pncp import LicitacaoAPI
import importlib
import pkgutil
import src.tools
from src.utils.metrics import start_metrics_server, REQUESTS, EXCEPTIONS, REQUEST_TIME
import src.utils.sentry

# Configuração do servidor MCP
server = Server("licitacoes-gov-br")

def importar_tools():
    for _, module_name, _ in pkgutil.iter_modules(src.tools.__path__):
        importlib.import_module(f"src.tools.{module_name}")

importar_tools()

start_metrics_server(port=8080)

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    return [
        Tool(
            name="buscar_licitacoes",
            description="Busca licitações governamentais com filtros opcionais",
            inputSchema={
                "type": "object",
                "properties": {
                    "termo": {"type": "string", "description": "Termo de busca (palavras-chave)"},
                    "orgao": {"type": "string", "description": "Nome ou código do órgão"},
                    "modalidade": {"type": "string", "description": "Modalidade (pregao, concorrencia, etc.)"},
                    "status": {"type": "string", "description": "Status da licitação (aberta, encerrada, etc.)"},
                    "valor_min": {"type": "number", "description": "Valor mínimo estimado"},
                    "valor_max": {"type": "number", "description": "Valor máximo estimado"}
                }
            }
        ),
        Tool(
            name="obter_detalhes_licitacao",
            description="Obtém detalhes completos de uma licitação específica",
            inputSchema={
                "type": "object",
                "properties": {
                    "numero_processo": {"type": "string", "description": "Número do processo licitatório", "required": True},
                    "fonte": {"type": "string", "description": "Fonte dos dados (pncp, comprasnet)", "default": "pncp"}
                },
                "required": ["numero_processo"]
            }
        ),
        Tool(
            name="listar_orgaos",
            description="Lista órgãos públicos disponíveis para consulta",
            inputSchema={
                "type": "object",
                "properties": {
                    "uf": {"type": "string", "description": "Unidade Federativa (sigla do estado)"}
                }
            }
        ),
        Tool(
            name="buscar_por_cnpj",
            description="Busca licitações relacionadas a um CNPJ específico",
            inputSchema={
                "type": "object",
                "properties": {
                    "cnpj": {"type": "string", "description": "CNPJ da empresa (com ou sem formatação)", "required": True}
                },
                "required": ["cnpj"]
            }
        ),
        Tool(
            name="estatisticas_licitacoes",
            description="Gera estatísticas sobre licitações em um período",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_inicio": {"type": "string", "description": "Data de início (YYYY-MM-DD)"},
                    "data_fim": {"type": "string", "description": "Data de fim (YYYY-MM-DD)"},
                    "orgao": {"type": "string", "description": "Filtrar por órgão específico"}
                }
            }
        )
    ]

@server.call_tool()
@REQUEST_TIME.time()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    REQUESTS.inc()
    async with LicitacaoAPI() as api_client:
        try:
            if name == "buscar_licitacoes":
                resultado = await api_client.buscar_pncp(
                    termo=arguments.get("termo", ""),
                    orgao=arguments.get("orgao", ""),
                    modalidade=arguments.get("modalidade", ""),
                    status=arguments.get("status", ""),
                    valor_min=arguments.get("valor_min", 0),
                    valor_max=arguments.get("valor_max", 0)
                )
                if "erro" in resultado:
                    response = f"❌ {resultado['erro']}"
                else:
                    licitacoes = resultado.get("dados", [])
                    if licitacoes:
                        response = f"✅ Encontradas {len(licitacoes)} licitações:\n\n"
                        for i, lic in enumerate(licitacoes[:10], 1):
                            response += f"{i}. **{lic.get('objeto', 'N/A')}**\n"
                            response += f"   📋 Processo: {lic.get('numero', 'N/A')}\n"
                            response += f"   🏢 Órgão: {lic.get('orgao', 'N/A')}\n"
                            response += f"   💰 Valor: R$ {lic.get('valor_estimado', 'N/A')}\n"
                            response += f"   📅 Abertura: {lic.get('data_abertura', 'N/A')}\n\n"
                    else:
                        response = "ℹ️ Nenhuma licitação encontrada com os critérios especificados."
            elif name == "obter_detalhes_licitacao":
                resultado = await api_client.obter_detalhes_licitacao(
                    numero_processo=arguments["numero_processo"],
                    fonte=arguments.get("fonte", "pncp")
                )
                if "erro" in resultado:
                    response = f"❌ {resultado['erro']}"
                else:
                    dados = resultado.get("dados", {})
                    response = "📋 **DETALHES DA LICITAÇÃO**\n\n"
                    response += f"**Número:** {dados.get('numero', 'N/A')}\n"
                    response += f"**Objeto:** {dados.get('objeto', 'N/A')}\n"
                    response += f"**Órgão:** {dados.get('orgao', 'N/A')}\n"
                    response += f"**Modalidade:** {dados.get('modalidade', 'N/A')}\n"
                    response += f"**Status:** {dados.get('status', 'N/A')}\n"
                    response += f"**Valor Estimado:** R$ {dados.get('valor_estimado', 'N/A')}\n"
                    response += f"**Data de Abertura:** {dados.get('data_abertura', 'N/A')}\n"
                    response += f"**Data de Encerramento:** {dados.get('data_encerramento', 'N/A')}\n"
                    if dados.get('itens'):
                        response += f"\n**Itens ({len(dados['itens'])}):**\n"
                        for item in dados['itens'][:5]:
                            response += f"• {item.get('descricao', 'N/A')}\n"
            elif name == "listar_orgaos":
                resultado = await api_client.listar_orgaos(
                    uf=arguments.get("uf", "")
                )
                if "erro" in resultado:
                    response = f"❌ {resultado['erro']}"
                else:
                    orgaos = resultado.get("dados", [])
                    response = f"🏢 **ÓRGÃOS DISPONÍVEIS** ({len(orgaos)})\n\n"
                    for orgao in orgaos[:20]:
                        response += f"• **{orgao.get('nome', 'N/A')}**\n"
                        response += f"  📍 {orgao.get('uf', 'N/A')} - {orgao.get('municipio', 'N/A')}\n"
                        response += f"  🆔 Código: {orgao.get('codigo', 'N/A')}\n\n"
            elif name == "buscar_por_cnpj":
                resultado = await api_client.buscar_por_cnpj(
                    cnpj=arguments["cnpj"]
                )
                if "erro" in resultado:
                    response = f"❌ {resultado['erro']}"
                else:
                    licitacoes = resultado.get("dados", [])
                    response = f"🔍 **LICITAÇÕES PARA CNPJ {arguments['cnpj']}**\n\n"
                    response += f"Encontradas {len(licitacoes)} licitações:\n\n"
                    for i, lic in enumerate(licitacoes[:10], 1):
                        response += f"{i}. {lic.get('objeto', 'N/A')}\n"
                        response += f"   📋 {lic.get('numero', 'N/A')}\n"
                        response += f"   💰 R$ {lic.get('valor', 'N/A')}\n\n"
            elif name == "estatisticas_licitacoes":
                resultado = await api_client.estatisticas_licitacoes(
                    data_inicio=arguments.get("data_inicio", ""),
                    data_fim=arguments.get("data_fim", ""),
                    orgao=arguments.get("orgao", "")
                )
                if "erro" in resultado:
                    response = f"❌ {resultado['erro']}"
                else:
                    response = (
                        "📊 **ESTATÍSTICAS DE LICITAÇÕES**\n\n"
                        f"Total de licitações: {resultado['total']}\n"
                        f"Valor total: R$ {resultado['valor_total']:.2f}\n"
                        f"Valor médio: R$ {resultado['valor_medio']:.2f}\n"
                    )
            else:
                response = f"❌ Ferramenta '{name}' não reconhecida."
        except Exception as e:
            EXCEPTIONS.inc()
            from src.utils.sentry import capture_exception
            capture_exception(e)
            response = f"❌ Erro interno: {str(e)}"
    return [types.TextContent(type="text", text=response)]

async def main():
    options = InitializationOptions(
        server_name="licitacoes-gov-br",
        server_version="1.0.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(
                tools_changed=True
            ),
            experimental_capabilities={}
        )
    )
    async with server.run_stdio() as server_process:
        await server_process.wait()

if __name__ == "__main__":
    asyncio.run(main()) 