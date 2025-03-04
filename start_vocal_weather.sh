#!/bin/zsh

# Définition des variables
backend_script="./start_backend.sh"
frontend_script="./start_frontend.sh"

# Ouvrir un terminal pour le backend
open -a Terminal "$backend_script"

# Attendre un peu que le backend démarre
sleep 5

# Ouvrir un terminal pour le frontend
open -a Terminal "$frontend_script"