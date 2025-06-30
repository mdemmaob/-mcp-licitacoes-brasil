from mcp.types import Tool, TextContent
from src.api.pncp import LicitacaoAPI
import pandas as pd
import os

@Tool(
    name="exportar_licitacoes_excel",
    description="Exporta resultados de busca de licitações para um arquivo Excel (xlsx)",
    inputSchema={
        "type": "object",
        "properties": {
            "termo": {"type": "string", "description": "Palavra-chave para busca"},
            "orgao": {"type": "string", "description": "Órgão"},
            "modalidade": {"type": "string", "description": "Modalidade"},
            "status": {"type": "string", "description": "Status"},
            "valor_min": {"type": "number", "description": "Valor mínimo"},
            "valor_max": {"type": "number", "description": "Valor máximo"}
        }
    }
)
async def exportar_licitacoes_excel_tool(arguments):
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_pncp(
            termo=arguments.get("termo", ""),
            orgao=arguments.get("orgao", ""),
            modalidade=arguments.get("modalidade", ""),
            status=arguments.get("status", ""),
            valor_min=arguments.get("valor_min", 0),
            valor_max=arguments.get("valor_max", 0)
        )
        licitacoes = resultado.get("dados", [])
        if not licitacoes:
            return [TextContent(type="text", text="Nenhuma licitação encontrada para exportar.")]
        df = pd.DataFrame(licitacoes)
        os.makedirs("exports", exist_ok=True)
        file_path = f"exports/licitacoes_export.xlsx"
        df.to_excel(file_path, index=False)
        return [TextContent(type="text", text=f"Exportação concluída: {file_path}")] 