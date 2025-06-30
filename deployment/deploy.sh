#!/bin/bash
# Script de deploy para MCP Licitações

echo "Parando serviço MCP..."
systemctl stop mcp-licitacoes

echo "Atualizando código..."
git pull

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Iniciando serviço MCP..."
systemctl start mcp-licitacoes

echo "Deploy concluído!" 