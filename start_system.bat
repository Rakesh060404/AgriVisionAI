@echo off
echo Starting Plant Disease Detection System...
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

echo Installing backend dependencies...
cd "%SCRIPT_DIR%backend"
pip install -r requirements.txt

echo.
echo Starting Flask backend server...
REM Use virtual environment Python if it exists, otherwise use system Python
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    start "Backend Server" cmd /k "cd /d "%SCRIPT_DIR%backend" && "%SCRIPT_DIR%.venv\Scripts\python.exe" backend.py"
) else (
    start "Backend Server" cmd /k "cd /d "%SCRIPT_DIR%backend" && python backend.py"
)

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting React frontend...
start "Frontend Server" cmd /k "cd /d "%SCRIPT_DIR%frontend" && npm run dev"

echo.
echo Both servers are starting up!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
pause
