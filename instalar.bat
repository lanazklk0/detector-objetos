@echo off
:: Create virtual environment
python -m venv .venv

:: Upgrade pip
.venv\Scripts\pip install --upgrade pip

:: Install required packages
.venv\Scripts\pip install faster-whisper ctranslate2 soundcard numpy webrtcvad argostranslate

:: Download and install the model
if not exist "translate-en_pt-br-1_9.argosmodel" (
    curl -L -o translate-en_pt-br-1_9.argosmodel https://example.com/path/to/translate-en_pt-br-1_9.argosmodel
)