from fastapi import FastAPI
from .routers import weather
from .config import API_KEY


app = FastAPI()

@app.get("/")
def hi():
    # a = normalyze_city("Kyiv")
    
    return {"message": f"Hello, {API_KEY}!"}

app.include_router(weather.router)