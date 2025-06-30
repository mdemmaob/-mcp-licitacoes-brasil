from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI

@Tool(
    name="buscar_por_cnpj",
    description="Busca licitações relacionadas a um CNPJ específico",
    inputSchema={
        "type": "object",
        "properties": {
            "cnpj": {"type": "string", "description": "CNPJ da empresa (com ou sem formatação)", "required": True}
        },
        "required": ["cnpj"]
    }
)
async def buscar_cnpj_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_por_cnpj(
            cnpj=arguments["cnpj"]
        )
        if "erro" in resultado:
            return [TextContent(type="text", text=f"❌ {resultado['erro']}")]
        licitacoes = resultado.get("dados", [])
        response = f"🔍 **LICITAÇÕES PARA CNPJ {arguments['cnpj']}**\n\n"
        response += f"Encontradas {len(licitacoes)} licitações:\n\n"
        for i, lic in enumerate(licitacoes[:10], 1):
            response += f"{i}. {lic.get('objeto', 'N/A')}\n"
            response += f"   📋 {lic.get('numero', 'N/A')}\n"
            response += f"   💰 R$ {lic.get('valor', 'N/A')}\n\n"
        return [TextContent(type="text", text=response)] 