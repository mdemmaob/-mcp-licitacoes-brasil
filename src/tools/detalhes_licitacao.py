from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI

@Tool(
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
)
async def detalhes_licitacao_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.obter_detalhes_licitacao(
            numero_processo=arguments["numero_processo"],
            fonte=arguments.get("fonte", "pncp")
        )
        if "erro" in resultado:
            return [TextContent(type="text", text=f"❌ {resultado['erro']}")]
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
        return [TextContent(type="text", text=response)] 