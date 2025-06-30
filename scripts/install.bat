@echo off
REM Script de instalação automatizada MCP Licitações Brasil (Windows)

cd /d %~dp0..

REM Verifica se o Python está instalado
where python >nul 2>nul || (
    echo Python não encontrado. Instale o Python 3.8+ antes de continuar.
    exit /b 1
)

REM Cria o ambiente virtual se não existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Instala as dependências
pip install --upgrade pip
pip install -r requirements.txt

REM Cria o arquivo .env se não existir
if not exist .env (
    copy .env.example .env
)

REM Mensagem final
echo.
echo Instalacao concluida!
echo Leia o arquivo docs\installation.md para mais instrucoes.
pause 