from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI

@Tool(
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
async def estatisticas_licitacoes_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.estatisticas_licitacoes(
            data_inicio=arguments.get("data_inicio", ""),
            data_fim=arguments.get("data_fim", ""),
            orgao=arguments.get("orgao", "")
        )
        if "erro" in resultado:
            return [TextContent(type="text", text=f"❌ {resultado['erro']}")]
        return [TextContent(
            type="text",
            text=(
                "📊 **ESTATÍSTICAS DE LICITAÇÕES**\n\n"
                f"Total de licitações: {resultado['total']}\n"
                f"Valor total: R$ {resultado['valor_total']:.2f}\n"
                f"Valor médio: R$ {resultado['valor_medio']:.2f}\n"
            )
        )] 