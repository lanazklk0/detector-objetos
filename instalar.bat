@echo off
setlocal EnableExtensions

echo ==========================================
echo  Instalando Legenda Offline (EN->PT-BR)
echo ==========================================
echo.

REM 1) Checar Python
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERRO] Python nao encontrado.
  echo Instale em: https://www.python.org/downloads/
  echo Marque "Add Python to PATH".
  pause
  exit /b 1
)

REM 2) Criar venv
if not exist .venv (
  echo Criando ambiente virtual (.venv)...
  python -m venv .venv
)

REM 3) Ativar venv e atualizar pip
call .venv\Scripts\activate
python -m pip install --upgrade pip

REM 4) Instalar dependencias
pip install faster-whisper ctranslate2 soundcard numpy webrtcvad argostranslate

REM 5) Baixar e instalar pacote Argos (EN -> PT-BR)
python -c "import urllib.request; url='https://github.com/argosopentech/argos-translate/releases/download/v1.9.6/translate-en_pt-br-1_9.argosmodel'; fn='translate-en_pt-br-1_9.argosmodel'; print('Baixando:', url); urllib.request.urlretrieve(url, fn); import argostranslate.package as pkg; pkg.install_from_path(fn); print('Modelo instalado OK')"

echo.
echo Instalacao concluida. Agora rode iniciar.bat
echo.
pause
endlocal