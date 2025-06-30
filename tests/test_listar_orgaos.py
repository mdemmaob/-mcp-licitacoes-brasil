import pytest
from api.pncp import LicitacaoAPI

@pytest.mark.asyncio
async def test_listar_orgaos():
    async with LicitacaoAPI() as api:
        resultado = await api.listar_orgaos(uf="DF")
        assert "dados" in resultado
        assert isinstance(resultado["dados"], list) 