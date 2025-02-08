CITY_MAP = {
    "Киев": "Kyiv",
    "Londn": "London",
    "Нью-Йорк": "New York",
    "Токио": "Tokyo"
}

def normalyze_city(city_name):
    return  CITY_MAP.get(city_name, city_name)