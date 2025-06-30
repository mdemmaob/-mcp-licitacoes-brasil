import pytest
from api.pncp import LicitacaoAPI
import os
import sys
import cProfile
import atexit
sys.path.insert(0, os.path.abspath('../src'))

profiler = cProfile.Profile()
profiler.enable()
atexit.register(lambda: profiler.dump_stats('profile.out'))

@pytest.mark.asyncio
async def test_fluxo_completo():
    async with LicitacaoAPI() as api:
        # 1. Buscar licitações com filtro
        resultado_busca = await api.buscar_pncp(termo="energia", status="aberta")
        assert "dados" in resultado_busca
        licitacoes = resultado_busca["dados"]
        assert isinstance(licitacoes, list)

        if licitacoes:
            # 2. Obter detalhes da primeira licitação encontrada
            numero_processo = licitacoes[0].get("numero")
            detalhes = await api.obter_detalhes_licitacao(numero_processo=numero_processo)
            assert "dados" in detalhes or "erro" in detalhes

            # 3. Buscar por órgão da licitação
            orgao = licitacoes[0].get("orgao")
            if orgao:
                orgaos = await api.listar_orgaos()
                assert "dados" in orgaos
                assert any(o.get("nome") == orgao for o in orgaos["dados"])

            # 4. Buscar por CNPJ se disponível
            cnpj = licitacoes[0].get("cnpj")
            if cnpj:
                cnpj_result = await api.buscar_por_cnpj(cnpj=cnpj)
                assert "dados" in cnpj_result or "erro" in cnpj_result

        # 5. Estatísticas gerais
        stats = await api.estatisticas_licitacoes()
        assert "total" in stats or "erro" in stats 