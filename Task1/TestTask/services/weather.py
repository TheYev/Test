import requests
from ..config import API_KEY


API_KEY = API_KEY
BASE_YRL = "http://api.openweathermap.org/data/2.5/weather?"

def fetch_weather(city):
    complete_url = BASE_YRL + "appid=" + API_KEY + "&q=" + city
    
    try:
        response = requests.get(complete_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
        
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None
    