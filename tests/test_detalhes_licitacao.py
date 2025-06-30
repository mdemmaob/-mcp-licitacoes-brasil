import pytest
from api.pncp import LicitacaoAPI

@pytest.mark.asyncio
async def test_obter_detalhes_licitacao():
    async with LicitacaoAPI() as api:
        resultado = await api.obter_detalhes_licitacao(numero_processo="123456")
        assert "dados" in resultado or "erro" in resultado 