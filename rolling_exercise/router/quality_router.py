from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controller.quality_controller import insert_data_from_csv
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

        response = insert_data_from_csv(db=db, df=clean_data)

        return JSONResponse(content=response, status_code=201)   
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading data - {e}")



# # Route to get a specific Alert
# @router.get("/{alert_id}", response_model=schemas.Alert)
# def get_alert_route(alert_id: int, db: Session = Depends(get_db)):
#     return get_alert(db=db, alert_id=alert_id)
