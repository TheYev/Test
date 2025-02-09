CITY_MAP = {
    "Киев": "Kyiv",
    "Londn": "London",
    "Нью-Йорк": "New York",
    "Токио": "Tokyo"
}
REGION_MAP = {
    "Europe": ["Kyiv", "London", "Paris", "Berlin", "Madrid"],
    "America": ["New York", "Los Angeles", "Toronto", "Mexico City"],
    "Asia": ["Tokyo", "Beijing", "Seoul", "Bangkok", "Delhi"],
    "Africa": ["Cairo", "Lagos", "Nairobi", "Johannesburg"],
    "Oceania": ["Sydney", "Melbourne", "Auckland"]
}

def normalyze_city(city_name: str) -> str:
    return  CITY_MAP.get(city_name, city_name)

def classify_region(city: str) -> str:
    for region, cities in REGION_MAP.items():
        if city in cities:
            return region
    return "Unknown"
