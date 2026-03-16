@echo off
color 0c
title ACE - CPA COMMAND CENTER
cls

echo ==================================================
echo   INITIALIZING AUTOMATED CONTENT ENGINE (ACE)...
echo ==================================================
:: Ensure dependencies are installed (Added static-ffmpeg)
pip install rich yt-dlp static-ffmpeg >nul 2>&1

:: Launch the main python script
python "%~dp0ACE.py"

:: When python script exits, close window
exit