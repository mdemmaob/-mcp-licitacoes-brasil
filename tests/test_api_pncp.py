import pytest
from src.api.pncp import LicitacaoAPI

@pytest.mark.asyncio
def test_buscar_pncp():
    import asyncio
    async def run():
        async with LicitacaoAPI() as api:
            resultado = await api.buscar_pncp(termo="energia")
            assert "dados" in resultado
            assert isinstance(resultado["dados"], list)
    asyncio.run(run()) 