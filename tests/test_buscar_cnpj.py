import pytest
from api.pncp import LicitacaoAPI

@pytest.mark.asyncio
async def test_buscar_por_cnpj():
    async with LicitacaoAPI() as api:
        resultado = await api.buscar_por_cnpj(cnpj="12345678000195")
        assert "dados" in resultado or "erro" in resultado 