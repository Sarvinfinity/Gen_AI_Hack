@echo off
cd /d "%~dp0"
echo ========================================
echo Starting Flask Server...
echo ========================================
echo.
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Please check if Python and Flask are installed correctly.
    pause
)
