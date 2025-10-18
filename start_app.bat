@echo off
setlocal

REM Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao foi encontrado. Instale o Python 3.10 ou superior a partir de https://www.python.org/downloads/ e execute este arquivo novamente.
    pause
    exit /b 1
)

REM Cria o ambiente virtual, se nao existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

REM Ativa o ambiente virtual
call .venv\Scripts\activate
if errorlevel 1 (
    echo Nao foi possivel ativar o ambiente virtual.
    pause
    exit /b 1
)

REM Instala dependencias
pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo Iniciando o servidor...
uvicorn app.main:app --host 0.0.0.0 --port 8000

if errorlevel 1 (
    echo O servidor foi encerrado com erro.
) else (
    echo Servidor finalizado.
)

pause
endlocal
