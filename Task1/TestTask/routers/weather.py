from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from celery.result import AsyncResult
from ..services.worker import fetch_weather
import uuid


class Cites(BaseModel):
    cities: list[str]

router = APIRouter()


@router.post("/weather", status_code=status.HTTP_201_CREATED)
async def weather(request: Cites):
    task_id = str(uuid.uuid4())
    data = fetch_weather.apply_async(args=[task_id, request.cities])
    
    if data is None:
        raise HTTPException(status_code=404, detail="City not found")
    return data

@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="WRong get request")
    return {"task_id": task_id, "status": result.state}

@router.get("/results/{region}", status_code=status.HTTP_200_OK)
async def get_results(region: str):
    filepath = f"weather_data/{region}"
    try:
        with open(filepath, "r") as file:
            data = file.read()
        return {"region": region, "data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="WRong get request")
