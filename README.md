# vocal-weather
Application météo par commande vocale

## Installation / config

### Cloner le dépôt

```bash
git clone <URL_DU_DEPOT>
   cd <NOM_DU_DEPOT
```

### Créer le fichier .env

```
# For Azure AI Services
SPEECH_KEY = *********
SPEECH_REGION = francecentral
# For Azure Storage Database
PATH_DONNEES = "./data"
NOM_BASES_DONNEES = "postgres"
USERAZURE = "cyril"
PASSWORD ="********"
HOST = "vw-cyril.postgres.database.azure.com"
PORT = "5432"
```

### Dans chacun des répertoires ./src/frontend et .src/backend :

```bash
 python3 -m venv ENV
 source ENV/bin/activate 
 pip install -r requirements.txt
```
###  Vous pouvez démarrer le front et le back en éxécutant
```bash
./start_vocal_weather.sh 
```
## OU

### Démarrer le backend
```bash  	
cd src/backend
./start_backend.sh
```

### Démarrer le frontend
```bash
cd src/frontend
./start_frontend.sh
```
