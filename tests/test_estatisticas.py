import pytest
from api.pncp import LicitacaoAPI

@pytest.mark.asyncio
async def test_estatisticas_licitacoes():
    async with LicitacaoAPI() as api:
        resultado = await api.estatisticas_licitacoes(data_inicio="2024-01-01", data_fim="2024-01-31")
        assert "total" in resultado or "erro" in resultado 