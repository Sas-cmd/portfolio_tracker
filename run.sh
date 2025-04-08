: '
@echo off
REM --- Windows CMD Section ---
echo Launching Portfolio Tracker...

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

streamlit run app\main.py
exit /b
'

# --- Unix Bash Section ---
echo "Launching Portfolio Tracker..."

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

streamlit run app/main.py