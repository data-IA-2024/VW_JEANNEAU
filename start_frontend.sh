#!/bin/zsh

frontend_path="$(cd "$(dirname "$0")" && pwd)/src/frontend"
frontend_appname="app"   # Nom du fichier Streamlit (ex: app.py)

# Aller dans le dossier du frontend et lancer Streamlit
cd "$frontend_path" || { echo "Erreur : dossier frontend introuvable !"; exit 1; }
echo "Démarrage du frontend Streamlit..."
source "./ENV/bin/activate"
streamlit run "$frontend_appname.py"   # Lancer en arrière-plan
exec zsh