from fastapi import FastAPI
from pydantic import BaseModel
import extract_lib
#import conversions as conv 
import open_meteo as mto
import fonctions_db as fdb
from datetime import datetime, timedelta

# Création de l'application FastAPI
app = FastAPI()


class TextInput(BaseModel):
    text: str

@app.post("/demande_meteo/")
def process_text(input: TextInput):
    print("text : ", input.text)
    if input.text == "":
        fdb.write_msg_DB("ERROR", "main.py : texte reçu vide")
        return {"text": "", "location": "", "date": "", "latitude": "", "longitude": "", "forecast": ""}
    else:
        fdb.write_msg_DB("INFO", f"main.py : texte reçu : {input.text}")
           
        # Extraction du lieu
        lieu = extract_lib.extract_location(input.text)
        if lieu == "":
            fdb.write_msg_DB("ERROR", "main.py : lieu non trouvé")
            lieu = "Tours"  # ici il faudrait geolocaliser l'utilisateur.
        else: 
            fdb.write_msg_DB("INFO", f"main.py : lieu trouvé : {lieu}")
        
        # Extraction de la date
        date = extract_lib.extract_date(input.text)

        if not date:
            fdb.write_msg_DB("ERROR", "main.py : date non trouvée")
            if datetime.now().hour > 12:    # Si demande à partir de 13:00, on considère que l'on veut la météo pour demain
                date = [("Demain", (datetime.now()+ timedelta(days=1)).date())]
                
            else:                           # Sinon, on considère que l'on veut la météo pour aujourd'hui
                date = [("Aujourd'hui", datetime.now().date())]
        
            fdb.write_msg_DB("INFO", f"main.py : date initilaisé par défaut: {date}")        
        else:
            #date_us = date[0][1].strftime("%Y-%m-%d")
            fdb.write_msg_DB("INFO", f"main.py : date trouvée : {date}")


        # Récupération des coordonnées GPS du lieu
        latitude, longitude = extract_lib.get_coordinates(lieu)
        if latitude == "" or longitude == "":
            fdb.write_msg_DB("ERROR", "main.py : coordonnées non trouvées")
            latitude = 47.394144 # Tours
            longitude = 0.68484 # Tours 
        else:
            fdb.write_msg_DB("INFO", f"main.py : coordonnées trouvées : {latitude}, {longitude}")      

        # Formatage de la date pour open-meteo YYYY-MM-DD
        #date_meteo = date.split("T")[0]
        date_obj = date[0][1]
        date_us = date_obj.strftime("%Y-%m-%d") 
        print()
        print(f"date : {date}")
        print(f"date_obj : {date_obj}")
        print(f"date : {date_us}")
        print()
        # Appel à l'API open-meteo
        ma_meteo = mto.get_weather(latitude, longitude, date_us)
        if ma_meteo == "":
            fdb.write_msg_DB("ERROR", "main.py : météo non trouvée")
        else:
            fdb.write_msg_DB("INFO", f"main.py : météo trouvée")
        #print(f"La temps pour {lieu} le {date_us} sera : {ma_meteo['temperature_max']}")

        # retourner les données météo
        print("text : ", input.text)
        print("location : ", lieu)
        print("date : ", date)
        print("latitude : ", latitude)
        print("longitude : ", longitude)
        print("forecast : ", ma_meteo)
                
        return {"text": input.text, "location": lieu, "date": date, "latitude": latitude, "longitude": longitude, "forecast": ma_meteo}
