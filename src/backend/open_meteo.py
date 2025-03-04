import requests

def get_weather(latitude: float, longitude: float, date: str):
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&start_date={date}&end_date={date}&timezone=Europe/Paris"
    response = requests.get(api_url)
    print(f"Requête envoyée à l'API : {api_url}")
    print(f"Statut de la réponse : {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Données reçues : {data}")
        
        if "daily" in data:
            daily_data = data["daily"]
            weather_info = {
                "date": date,
                "temperature_max": daily_data["temperature_2m_max"][0],
                "temperature_min": daily_data["temperature_2m_min"][0],
                "precipitation": daily_data["precipitation_sum"][0],
                "windspeed_max": daily_data["windspeed_10m_max"][0]
            }
            return weather_info
        else:
            raise Exception("Weather data not found")
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

if __name__ == "__main__":

    #Code de test
    latitude = 48.8566  # Latitude de Paris
    longitude = 2.3522  # Longitude de Paris
    date = "2025-02-28"  # Date pour laquelle obtenir la météo
    try:
        weather_info = get_weather(latitude, longitude, date)
        print(f"Météo pour {date} : {weather_info}")
    except Exception as e:
        print(e)