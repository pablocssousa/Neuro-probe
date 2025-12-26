@echo off
REM Neuro-Probe Launcher for Windows
echo.
echo ============================================================
echo           NEURO-PROBE v1.0.0
echo      Emulator Behavior Analysis Tool
echo ============================================================
echo.

python neuro-probe.py %*

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch Neuro-Probe
    echo Make sure Python 3.7+ is installed
    pause
)
