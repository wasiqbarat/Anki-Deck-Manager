@echo off
echo Stopping Anki Deck Manager...
docker-compose down
echo "Anki Deck Manager has been stopped."
timeout /t 3 /nobreak >nul
