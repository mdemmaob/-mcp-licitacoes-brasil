# 🏛️ MCP Licitações Governamentais

[![CI](https://github.com/seu-usuario/mcp-licitacoes-brasil/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/mcp-licitacoes-brasil/actions)
[![Lint](https://github.com/seu-usuario/mcp-licitacoes-brasil/actions/workflows/lint.yml/badge.svg)](https://github.com/seu-usuario/mcp-licitacoes-brasil/actions)
[![Coverage Status](https://codecov.io/gh/seu-usuario/mcp-licitacoes-brasil/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/mcp-licitacoes-brasil)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

Servidor MCP para consulta de licitações públicas brasileiras, integrando APIs oficiais como PNCP e ComprasNet. Pronto para uso com Claude Desktop e fácil de expandir para novas fontes e ferramentas.

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mcp-licitacoes-brasil.git
cd mcp-licitacoes-brasil
# Crie o ambiente virtual
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
# Instale as dependências
pip install -r requirements.txt
```

---

## ⚙️ Configuração

1. Edite os arquivos em `config/` conforme seu ambiente (development.yaml, production.yaml, apis_endpoints.yaml).
2. Configure o Claude Desktop conforme exemplo abaixo:

```json
{
  "mcpServers": {
    "licitacoes-gov-br": {
      "command": "python",
      "args": ["src/main.py"],
      "cwd": "/caminho/para/mcp_licitacoes",
      "env": {
        "PYTHONPATH": "/caminho/para/mcp_licitacoes"
      }
    }
  }
}
```

---

## ▶️ Como Rodar

```bash
python src/main.py
```

---

## 🛠️ Ferramentas Disponíveis

- **buscar_licitacoes**: Busca licitações com múltiplos filtros
- **obter_detalhes_licitacao**: Detalhes completos de uma licitação
- **listar_orgaos**: Lista órgãos públicos disponíveis
- **buscar_por_cnpj**: Histórico de participação de empresa
- **estatisticas_licitacoes**: Relatórios e estatísticas

---

## 📦 Estrutura de Diretórios

```
src/
  api/           # Integrações com APIs
  models/        # Modelos de dados
  tools/         # Ferramentas MCP
  cache/         # Implementação de cache
  utils/         # Utilitários
  main.py        # Servidor MCP principal
  config.py      # Configuração centralizada
config/          # Arquivos de configuração
data/            # Dados auxiliares
examples/        # Exemplos de uso
docs/            # Documentação detalhada
tests/           # Testes automatizados
deployment/      # Scripts e configs de deploy
logs/            # Logs da aplicação
```

---

## 🌐 APIs Integradas

- **PNCP**: https://pncp.gov.br/api/consulta/v1
- **ComprasNet**: https://compras.dados.gov.br/api/v1

---

## 🧪 Testes

Para rodar todos os testes:
```bash
pytest tests/
```

---

## 🤝 Contribuindo

Pull requests são bem-vindos! Veja o arquivo `CONTRIBUTING.md` para detalhes.

---

## 📄 Licença

MIT

---

## 📚 Mais informações

- [Documentação oficial do MCP](https://modelcontextprotocol.io/)
- [Documentação do PNCP](https://pncp.gov.br/api/docs)
- [Documentação do ComprasNet](https://compras.dados.gov.br/docs) 