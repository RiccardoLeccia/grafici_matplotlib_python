@echo off
echo ===================================================
echo Creazione ambiente virtuale e installazione librerie
echo ===================================================

if not exist .venv (
    echo Creazione della cartella .venv...
    python -m venv .venv
)

echo Aggiornamento pip e installazione librerie da requirements.txt...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ===================================================
echo Installazione completata con successo!
echo ===================================================
pause