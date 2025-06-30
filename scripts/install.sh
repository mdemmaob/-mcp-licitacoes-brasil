#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "🚀 Instalando MCP Licitações Brasil..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale o Python 3.8+ primeiro."
    exit 1
fi

# Criar ambiente virtual
if [ ! -d venv ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variáveis de ambiente
if [ ! -f .env ]; then
    echo "⚙️ Criando arquivo .env..."
    cp .env.example .env
fi

echo "✅ Instalação concluída!"
echo "📖 Leia docs/installation.md para configurar o Claude Desktop" 