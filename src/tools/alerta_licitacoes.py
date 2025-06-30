from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI
from src.api.tce_sp import TCESPAPI
from src.utils.notify import send_telegram_alert

@Tool(
    name="alerta_licitacoes",
    description="Envia alerta para novas licitações que correspondam a filtros definidos",
    inputSchema={
        "type": "object",
        "properties": {
            "termo": {"type": "string", "description": "Palavra-chave para alerta"},
            "orgao": {"type": "string", "description": "Órgão de interesse"}
        }
    }
)
async def alerta_licitacoes_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_pncp(
            termo=arguments.get("termo", ""),
            orgao=arguments.get("orgao", "")
        )
        licitacoes = resultado.get("dados", [])
        if licitacoes:
            msg = f"Alerta: {len(licitacoes)} novas licitações para '{arguments.get('termo')}'"
            send_telegram_alert(msg)
            return [TextContent(type="text", text=msg)]
        return [TextContent(type="text", text="Nenhuma nova licitação encontrada.")]

@Tool(
    name="buscar_licitacoes_tce_sp",
    description="Busca licitações no TCE-SP por palavra-chave",
    inputSchema={
        "type": "object",
        "properties": {
            "termo": {"type": "string", "description": "Palavra-chave para busca"}
        }
    }
)
async def buscar_licitacoes_tce_sp_tool(arguments):
    async with TCESPAPI() as api:
        resultado = await api.buscar_licitacoes(termo=arguments.get("termo", ""))
        licitacoes = resultado.get("dados", [])
        if licitacoes:
            response = f"Encontradas {len(licitacoes)} licitações no TCE-SP."
        else:
            response = "Nenhuma licitação encontrada no TCE-SP."
        return [TextContent(type="text", text=response)] 