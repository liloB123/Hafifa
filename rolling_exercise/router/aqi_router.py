from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controller.aqi_controller import get_aqi_by_city, get_aqi_average, get_best_cities
import schemas
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
from io import StringIO
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/city", status_code=200)
def get_aqi_by_city_router(city: str,  db: Session = Depends(get_db)):
    try:
        return get_aqi_by_city(db, city)
    except HTTPException as e:
        raise e
    
@router.get("/city/average", status_code=200)
def get_average_aqi_by_city(city: str, db: Session = Depends(get_db)):
    try:
        return f"The avergae aqi in {city} is {get_aqi_average(db, city)}"
    except HTTPException as e:
        raise e

@router.get("/best", status_code=200)
def get_best_cities_router(db: Session = Depends(get_db)):
    try:
        return f"The cities that have the best air conditions are {get_best_cities(db)}"
    except HTTPException as e:
        raise e