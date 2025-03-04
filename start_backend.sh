#!/bin/zsh

backend_path="$(cd "$(dirname "$0")" && pwd)/src/backend"
backend_appname="main"  # Nom du fichier FastAPI (ex: main.py)

cd "$backend_path" || { echo "Erreur : dossier backend introuvable !"; exit 1; }
echo "🚀 Démarrage du backend FastAPI..."
source "./ENV/bin/activate"
uvicorn "$backend_appname":app --host localhost --port 8000
exec zsh
