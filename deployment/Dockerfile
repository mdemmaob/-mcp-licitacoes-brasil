# Dockerfile para MCP Licitações Governamentais
FROM python:3.11-slim

WORKDIR /app

# Copia o código do projeto
COPY . /app

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expõe a porta padrão (ajuste se necessário)
EXPOSE 8080

# Comando para iniciar o servidor MCP
CMD ["python", "src/main.py"] 