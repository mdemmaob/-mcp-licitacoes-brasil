# Exemplo de uso básico do MCP Licitações
from src.api.pncp import LicitacaoAPI
import asyncio

async def main():
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_pncp(termo="energia")
        print(resultado)

if __name__ == "__main__":
    asyncio.run(main()) 