import pytest
from api.pncp import LicitacaoAPI

@pytest.mark.asyncio
async def test_buscar_licitacoes():
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_pncp(termo="energia")
        assert "dados" in resultado
        assert isinstance(resultado["dados"], list) 