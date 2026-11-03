@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:4173 in your browser. Press Ctrl+C to stop.
py -3 scripts\serve.py --port 4173
if errorlevel 1 pause
