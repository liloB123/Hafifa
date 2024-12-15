from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controller.quality_controller import insert_data_from_csv, get_qaulity_by_date, get_quality_by_city
import schemas
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
from io import StringIO
from fastapi.responses import JSONResponse
from functions import logger

router = APIRouter()

@router.post("/", status_code=201)
async def upload_data_route(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        stringio = StringIO(contents.decode()) 
        data = pd.read_csv(stringio)
        clean_data = data.dropna()
        corrupted_data = data[~data.index.isin(clean_data.index)]
        logger.info(f"corrupted lines - {corrupted_data}")

        response = await insert_data_from_csv(db=db, df=clean_data)

        return JSONResponse(content=response, status_code=201)   
    except HTTPException as e:
        raise e

@router.get("/date", status_code=200)
def get_quality_by_date_route(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        return get_qaulity_by_date(db, start_date, end_date)
    except HTTPException as e:
        raise e
    
@router.get("/city", status_code=200)
def get_quality_by_city_route(city: str, db: Session = Depends(get_db)):
    try:
        return get_quality_by_city(db, city)
    except HTTPException as e:
        raise e
