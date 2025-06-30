# Tutorial de Uso - MCP Licitações

## 1. Instalação

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
pip install -r requirements.txt
```

## 2. Configuração

Edite os arquivos em `config/` conforme seu ambiente.

## 3. Executando o servidor

```bash
python src/main.py
```

## 4. Exemplos de uso

- Buscar licitações:
  ```json
  { "tool": "buscar_licitacoes", "args": { "termo": "energia" } }
  ```
- Detalhar licitação:
  ```json
  { "tool": "obter_detalhes_licitacao", "args": { "numero_processo": "2024-0001" } }
  ```

Consulte a [referência de API](api_reference.md) para mais exemplos. 