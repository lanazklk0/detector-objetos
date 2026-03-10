@echo off
REM Create virtual environment if it doesn't exist
if not exist .venv (
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install required packages
pip install -r requirements.txt

REM Download Argos model
if not exist translate-en_pt-br-1_9.argosmodel (
    curl -L -o translate-en_pt-br-1_9.argosmodel https://github.com/argosopentech/argos-translate/releases/download/v1.9.6/translate-en_pt-br-1_9.argosmodel
)

REM Install Argos model
python -c "import argostranslate; argostranslate.package.install_from_path('translate-en_pt-br-1_9.argosmodel')"

pause

REM Error Check
if %errorlevel% neq 0 (
    echo Error occurred during installation of Argos model.
    exit /b 1
)

echo Installation Complete!