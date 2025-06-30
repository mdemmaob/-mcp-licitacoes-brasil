import httpx
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
import os
from src.utils.logger import get_logger

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

APIS = {
    "pncp": "https://pncp.gov.br/api/consulta/v1",
    "comprasnet": "https://compras.dados.gov.br/api/v1",
    "tce_sp": "https://api.tce.sp.gov.br/v1"
}

cache = {}
CACHE_DURATION = CACHE_TTL  # 5 minutos

logger = get_logger(__name__)

class LicitacaoAPI:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info("LicitacaoAPI inicializada")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def _cache_key(self, endpoint: str, params: Dict) -> str:
        return f"{endpoint}:{hash(frozenset(params.items()))}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        return (datetime.now().timestamp() - timestamp) < CACHE_DURATION

    async def buscar_pncp(self, termo: str = "", orgao: str = "", modalidade: str = "", status: str = "", valor_min: float = 0, valor_max: float = 0) -> Dict:
        params = {}
        if termo:
            params["termo"] = termo
        if orgao:
            params["orgao"] = orgao
        if modalidade:
            params["modalidade"] = modalidade
        if status:
            params["status"] = status
        if valor_min > 0:
            params["valorMinimo"] = valor_min
        if valor_max > 0:
            params["valorMaximo"] = valor_max
        cache_key = self._cache_key("pncp_busca", params)
        if cache_key in cache and self._is_cache_valid(cache[cache_key]["timestamp"]):
            return cache[cache_key]["data"]
        try:
            url = f"{APIS['pncp']}/licitacoes"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            cache[cache_key] = {
                "data": data,
                "timestamp": datetime.now().timestamp()
            }
            logger.info(f"Busca PNCP realizada com sucesso: {params}")
            return data
        except httpx.RequestError as e:
            logger.error(f"Erro na requisição PNCP: {str(e)}")
            return {"erro": f"Erro na requisição PNCP: {str(e)}", "dados": []}
        except Exception as e:
            logger.error(f"Erro inesperado: {str(e)}")
            return {"erro": f"Erro inesperado: {str(e)}", "dados": []}

    async def obter_detalhes_licitacao(self, numero_processo: str, fonte: str = "pncp") -> Dict:
        cache_key = self._cache_key(f"{fonte}_detalhes", {"processo": numero_processo})
        if cache_key in cache and self._is_cache_valid(cache[cache_key]["timestamp"]):
            return cache[cache_key]["data"]
        try:
            if fonte == "pncp":
                url = f"{APIS['pncp']}/licitacoes/{numero_processo}"
            elif fonte == "comprasnet":
                url = f"{APIS['comprasnet']}/licitacoes/{numero_processo}"
            else:
                return {"erro": "Fonte não suportada", "dados": {}}
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            cache[cache_key] = {
                "data": data,
                "timestamp": datetime.now().timestamp()
            }
            return data
        except httpx.RequestError as e:
            return {"erro": f"Erro na requisição: {str(e)}", "dados": {}}
        except Exception as e:
            return {"erro": f"Erro inesperado: {str(e)}", "dados": {}}

    async def listar_orgaos(self, uf: str = "") -> Dict:
        params = {"uf": uf} if uf else {}
        cache_key = self._cache_key("orgaos", params)
        if cache_key in cache and self._is_cache_valid(cache[cache_key]["timestamp"]):
            return cache[cache_key]["data"]
        try:
            url = f"{APIS['pncp']}/orgaos"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            cache[cache_key] = {
                "data": data,
                "timestamp": datetime.now().timestamp()
            }
            return data
        except Exception as e:
            return {"erro": f"Erro ao listar órgãos: {str(e)}", "dados": []}

    async def buscar_por_cnpj(self, cnpj: str) -> Dict:
        cache_key = self._cache_key("cnpj", {"cnpj": cnpj})
        if cache_key in cache and self._is_cache_valid(cache[cache_key]["timestamp"]):
            return cache[cache_key]["data"]
        try:
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            url = f"{APIS['pncp']}/fornecedores/{cnpj_limpo}/licitacoes"
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            cache[cache_key] = {
                "data": data,
                "timestamp": datetime.now().timestamp()
            }
            return data
        except Exception as e:
            return {"erro": f"Erro na busca por CNPJ: {str(e)}", "dados": []}

    async def estatisticas_licitacoes(self, data_inicio: str = "", data_fim: str = "", orgao: str = "") -> Dict:
        params = {}
        if data_inicio:
            params["dataInicio"] = data_inicio
        if data_fim:
            params["dataFim"] = data_fim
        if orgao:
            params["orgao"] = orgao
        try:
            url = f"{APIS['pncp']}/licitacoes"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            licitacoes = data.get("dados", [])
            total = len(licitacoes)
            valor_total = sum(l.get("valor_estimado", 0) or 0 for l in licitacoes)
            valor_medio = valor_total / total if total else 0
            return {
                "total": total,
                "valor_total": valor_total,
                "valor_medio": valor_medio
            }
        except Exception as e:
            return {"erro": f"Erro ao gerar estatísticas: {str(e)}"}

def get_cache():
    from .memory_cache import MemoryCache
    from .redis_cache import RedisCache
    import os
    if os.getenv("USE_REDIS_CACHE", "false").lower() == "true":
        return RedisCache()
    return MemoryCache() 