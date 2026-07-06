@echo off
chcp 65001 >nul 2>&1
title PaveVision Public Web Demo

setlocal
set "PROJECT_PATH=%~dp0"
set "PYTHON_BIN=python"

if defined PAVEVISION_PYTHON (
    set "PYTHON_BIN=%PAVEVISION_PYTHON%"
)

cd /d "%PROJECT_PATH%"
if errorlevel 1 (
    echo [ERROR] Failed to enter repository directory.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   PaveVision public web demo
echo ============================================================
echo.

%PYTHON_BIN% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo   Flask is not installed. Installing web demo dependencies...
    %PYTHON_BIN% -m pip install -r web_demo\requirements.txt
    if errorlevel 1 (
        echo.
        echo   [ERROR] Dependency installation failed.
        echo.
        pause
        exit /b 1
    )
)

echo   Starting demo at http://localhost:5000
echo   Press Ctrl+C in this window to stop the server.
echo.

start "" /b cmd /c "timeout /t 3 >nul && start http://localhost:5000"
cd /d "%PROJECT_PATH%web_demo"
%PYTHON_BIN% app.py

endlocal
