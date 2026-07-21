@echo off
REM MotoERP Quick Start Script for Windows
REM Automează setup local în 3 comenzi

setlocal enabledelayedexpansion

echo.
echo 🚀 MotoERP - Quick Start (Windows)
echo ===================================
echo.

REM 1. Creează .env din template
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env with your Supabase credentials:
    echo    SUPABASE_URL=https://xxxxx.supabase.co
    echo    SUPABASE_KEY=eyJhbGc...
    echo.
) else (
    echo ✅ .env already exists
)

REM 2. Create virtual environment
if not exist venv (
    echo 🐍 Creating Python virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

REM 3. Activate venv and install dependencies
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Edit .env with Supabase credentials
echo 2. Run Supabase schema: database/schema.sql
echo 3. Start app: streamlit run app/app.py
echo.
echo 🌐 App will open at: http://localhost:8501
echo.
pause
