from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from dateparser.search import search_dates
from datetime import datetime, timedelta
import dateparser
import requests

# Charger le modèle CamemBERT pour l'extraction des entités nommées
tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates", cache_dir="./cache")
model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


# Fonction d'extraction des entités lieu("LOC") avec CamemBERT
def extract_location(text):
    
    entities = nlp(text)
    places = [ent['word'] for ent in entities if ent['entity_group'] == "LOC"]
    print (places)

    if places == []:
        return "Tours"  # ici il faut geolocaliser l'utilisateur.
    return places[0]


# Fonction d'extraction des dates avec dateparser
def extract_date(text):
    # Configuration de dateparser pour le français
    dateparser_settings = {
        'PREFER_DATES_FROM': 'future',
        'RELATIVE_BASE': datetime.now(),
        'TIMEZONE': 'Europe/Paris',
        'RETURN_AS_TIMEZONE_AWARE': True,
        'PREFER_DAY_OF_MONTH': 'current',
        'DATE_ORDER': 'DMY'
    }
    # Extraction des dates avec dateparser
    dates = search_dates(text, languages=['fr'], settings=dateparser_settings)
    
   

    # Ajout des expressions manquantes relatives aux dates
    # Pourra être ajusté en fonction des retours utilisateurs ou du monitoring
    missing_expressions = {
        "la semaine prochaine": datetime.now() + timedelta(days=7),
        "fin de semaine": datetime.now() + timedelta((5 - datetime.now().weekday()) % 7),
        "ce week-end": datetime.now() + timedelta((5 - datetime.now().weekday()) % 7)
    }

    for phrase, date in missing_expressions.items():
        if phrase in text:
            if dates:
                dates.append((phrase, date))
            else:
                dates = [(phrase, date)]
    
    return dates


# Fonction de récupération des coordonnées GPS d'une ville avec OpenStreetMap
def get_coordinates(city: str):
     
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1&countrycodes=FR"
    headers = {
        "User-Agent": "test_app_VW/1.0 (cyril.jeanneau@gmail.com)" 
    }
    response = requests.get(url, headers=headers)
    print(f"Requête envoyée à l'API : {url}")
    print(f"Statut de la réponse : {response.status_code}")

    if response.status_code == 200:
        print(response.status_code)
        data = response.json()
        print(data)
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            raise Exception("City not found")
    else:
        raise Exception("Error fetching coordinates")
