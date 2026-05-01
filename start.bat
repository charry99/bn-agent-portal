@echo off
REM Startup script for Billions Network Agent Portal (Windows)

echo ======================================
echo Billions Network Agent Portal
echo Starting Application...
echo ======================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Installing/Updating dependencies...
pip install -q -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist logs mkdir logs
if not exist uploads mkdir uploads
if not exist instance mkdir instance

REM Load environment variables from .env if it exists
if exist .env (
    echo Loading environment variables from .env
    for /f "tokens=*" %%i in (.env) do (
        if not "%%i"=="" (
            if not "%%i:~0,1%"=="#" (
                set "%%i"
            )
        )
    )
) else (
    echo WARNING: .env file not found. Create one from .env.example
    echo copy .env.example .env
    exit /b 1
)

REM Set defaults if not in .env
if not defined FLASK_ENV set FLASK_ENV=development
if not defined PORT set PORT=5000
if not defined HOST set HOST=0.0.0.0

REM Initialize database if needed
if not exist "instance\agent_portal.db" (
    echo Initializing database...
    python -m flask init-db
    echo Database initialized!
)

REM Display startup information
echo.
echo ======================================
echo Configuration:
echo   Environment: %FLASK_ENV%
echo   Debug Mode: %DEBUG%
echo   Host: %HOST%:%PORT%
echo ======================================
echo.

REM Start the application
if "%FLASK_ENV%"=="production" (
    echo Starting production server with Gunicorn...
    gunicorn --bind %HOST%:%PORT% --workers 4 --timeout 120 "app:create_app()"
) else (
    echo Starting development server...
    echo Application available at http://localhost:%PORT%
    echo Press CTRL+C to stop
    echo.
    python -m flask run --host=%HOST% --port=%PORT%
)

pause
