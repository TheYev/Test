from fastapi import APIRouter, HTTPException
from ..services.weather import featch_weather
from pydantic import BaseModel


class Cites(BaseModel):
    city: str

router = APIRouter()

@router.post("/weather")
async def weather():
    data = featch_weather("London")
    
    if data is None:
        raise HTTPException(status_code=404, detail="City not found")
    return data

@router.get("/tasks/{task_id}")
async def read_item_by_id(task_id: int):
    pass

@router.get("results/{region}")
async def get_results_by_region(region: str):
    pass
