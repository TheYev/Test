from fastapi import FastAPI
from .routers import weather
from .config import API_KEY
from .utils.city_utils import normalyze_city, classify_region


app = FastAPI()

@app.get("/")
def hi():
    a = normalyze_city("Kyiv")
    b = classify_region(a)
    
    return {"message": f"Hello, {b}!"}

app.include_router(weather.router)