@echo off
title EduGenie Server
cd /d "%~dp0"

echo ===================================================
echo     Starting EduGenie AI Learning Assistant...
echo ===================================================

if not exist ".env" (
    echo [.env] not found. Creating .env from .env.example...
    copy .env.example .env
)

echo.
echo Opening EduGenie in your browser...
start http://127.0.0.1:8000

echo Launching Uvicorn Server...
echo.
venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
