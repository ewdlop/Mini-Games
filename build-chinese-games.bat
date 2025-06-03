@echo off
REM Build Chinese Python Games - Batch Wrapper
REM This batch file runs the PowerShell script to build Chinese Python games

echo.
echo === Chinese Python Games Builder ===
echo.

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: PowerShell is not available or not in PATH
    echo Please ensure PowerShell is installed and accessible
    pause
    exit /b 1
)

REM Set execution policy for current session (in case it's restricted)
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force"

REM Run the PowerShell script
echo Running PowerShell script...
powershell -ExecutionPolicy Bypass -File "build-chinese-games.ps1" %*

if %ERRORLEVEL% equ 0 (
    echo.
    echo Build completed successfully!
    echo Check the 'release' directory for your executable games.
) else (
    echo.
    echo Build failed! Check the output above for details.
)

echo.
pause 