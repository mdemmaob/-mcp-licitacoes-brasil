from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI

@Tool(
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
)
async def buscar_licitacoes_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_pncp(
            termo=arguments.get("termo", ""),
            orgao=arguments.get("orgao", ""),
            modalidade=arguments.get("modalidade", ""),
            status=arguments.get("status", ""),
            valor_min=arguments.get("valor_min", 0),
            valor_max=arguments.get("valor_max", 0)
        )
        if "erro" in resultado:
            return [TextContent(type="text", text=f"❌ {resultado['erro']}")]
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
        return [TextContent(type="text", text=response)] 