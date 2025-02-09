from celery import Celery
import time
from .weather import fetch_weather
from ..utils.city_utils import normalyze_city, classify_region
import json
import os


celery_app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery_app.task(bind=True)
def process_weather_task(task_id, cities):
    results = {"Europe": [], "America": [], "Asia": [], "Africa": [], "Oceania": []}

    for city in cities:
        norm_city = normalyze_city(city)
        data = fetch_weather(norm_city)
        if not data or not (-350 <= data["temperature"] <= 350):
            continue

        region = classify_region(norm_city)
        if region != "Unknown":
            results[region].append(data)

    output_dir = f"weather_data/{task_id}"
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/results.json", "w") as f:
        json.dump(results, f)

    return results
