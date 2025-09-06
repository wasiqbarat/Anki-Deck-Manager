@echo off
echo Starting Anki Deck Manager...
docker-compose up -d
timeout /t 5 /nobreak >nul
start http://localhost:8501
echo "Anki Deck Manager is now running at http://localhost:8501"
pause
