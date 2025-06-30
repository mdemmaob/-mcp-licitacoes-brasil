# 📚 Referência de API - MCP Licitações

## buscar_licitacoes

**Payload de exemplo:**
```json
{
  "tool": "buscar_licitacoes",
  "args": {
    "termo": "equipamentos médicos",
    "modalidade": "pregao",
    "status": "aberta",
    "valor_min": 50000
  }
}
```
**Resposta de exemplo:**
```json
{
  "text": "✅ Encontradas 3 licitações:\n\n1. **Aquisição de equipamentos médicos**\n   📋 Processo: 2024-0001\n   🏢 Órgão: Ministério da Saúde\n   💰 Valor: R$ 120000.00\n   📅 Abertura: 2024-07-10\n\n..."
}
```

---

## obter_detalhes_licitacao

**Payload de exemplo:**
```json
{
  "tool": "obter_detalhes_licitacao",
  "args": {
    "numero_processo": "2024-0001",
    "fonte": "pncp"
  }
}
```
**Resposta de exemplo:**
```json
{
  "text": "📋 **DETALHES DA LICITAÇÃO**\n\n**Número:** 2024-0001\n**Objeto:** Aquisição de equipamentos médicos\n**Órgão:** Ministério da Saúde\n**Modalidade:** Pregão\n**Status:** Aberta\n**Valor Estimado:** R$ 120000.00\n**Data de Abertura:** 2024-07-10\n**Data de Encerramento:** 2024-07-20\n\n**Itens (2):**\n• Monitor cardíaco\n• Respirador hospitalar\n"
}
```

---

## listar_orgaos

**Payload de exemplo:**
```json
{
  "tool": "listar_orgaos",
  "args": {
    "uf": "DF"
  }
}
```
**Resposta de exemplo:**
```json
{
  "text": "🏢 **ÓRGÃOS DISPONÍVEIS** (2)\n\n• **Ministério da Saúde**\n  📍 DF - Brasília\n  🆔 Código: 1234\n\n• **Ministério da Educação**\n  📍 DF - Brasília\n  🆔 Código: 5678\n"
}
```

---

## buscar_por_cnpj

**Payload de exemplo:**
```json
{
  "tool": "buscar_por_cnpj",
  "args": {
    "cnpj": "12345678000195"
  }
}
```
**Resposta de exemplo:**
```json
{
  "text": "🔍 **LICITAÇÕES PARA CNPJ 12345678000195**\n\nEncontradas 2 licitações:\n\n1. Aquisição de insumos\n   📋 2024-0002\n   💰 R$ 50000.00\n\n2. Serviços de manutenção\n   📋 2024-0003\n   💰 R$ 30000.00\n"
}
```

---

## estatisticas_licitacoes

**Payload de exemplo:**
```json
{
  "tool": "estatisticas_licitacoes",
  "args": {
    "data_inicio": "2024-01-01",
    "data_fim": "2024-01-31"
  }
}
```
**Resposta de exemplo:**
```json
{
  "text": "📊 **ESTATÍSTICAS DE LICITAÇÕES**\n\nTotal de licitações: 15\nValor total: R$ 1.200.000,00\nValor médio: R$ 80.000,00\n"
}
``` 