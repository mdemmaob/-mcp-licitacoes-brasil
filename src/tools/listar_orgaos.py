from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI

@Tool(
    name="listar_orgaos",
    description="Lista órgãos públicos disponíveis para consulta",
    inputSchema={
        "type": "object",
        "properties": {
            "uf": {"type": "string", "description": "Unidade Federativa (sigla do estado)"}
        }
    }
)
async def listar_orgaos_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.listar_orgaos(
            uf=arguments.get("uf", "")
        )
        if "erro" in resultado:
            return [TextContent(type="text", text=f"❌ {resultado['erro']}")]
        orgaos = resultado.get("dados", [])
        response = f"🏢 **ÓRGÃOS DISPONÍVEIS** ({len(orgaos)})\n\n"
        for orgao in orgaos[:20]:
            response += f"• **{orgao.get('nome', 'N/A')}**\n"
            response += f"  📍 {orgao.get('uf', 'N/A')} - {orgao.get('municipio', 'N/A')}\n"
            response += f"  🆔 Código: {orgao.get('codigo', 'N/A')}\n\n"
        return [TextContent(type="text", text=response)] 