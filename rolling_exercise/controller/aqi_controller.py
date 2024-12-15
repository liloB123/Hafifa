from sqlalchemy.orm import Session
import pandas as pd
import models
from fastapi import HTTPException
from functions import logger, calculate_aqi, validate_query_params
import numpy as np

def get_aqi_by_city(db: Session, city: str):
    try:
        missing_params = validate_query_params({
            "city" : city,
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        aqis = get_aqis(db, city)

        if aqis:
            logger.info(f"{len(aqis)} aqis were returned for the city {city}")
            return aqis
        
        logger.error(f"There is no data about the aqi of the city {city}")
        raise HTTPException(status_code=404, detail="There is no data about the aqi for this city")
    except HTTPException as e:
        raise e

def get_aqi_average(db: Session, city: str):
    try:
        missing_params = validate_query_params({
            "city" : city,
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        aqis = get_aqis(db, city)
        avergae = np.average(aqis)

        if aqis:
            logger.info(f"Avergae aqi was returned for the city {city}")
            return avergae
        
        logger.error(f"There is no data about the aqi of the city {city}")
        raise HTTPException(status_code=404, detail="There is no data about the aqi for this city")

    except HTTPException as e:
        raise e

def get_aqis(db: Session, city: str):
    try:
        missing_params = validate_query_params({
            "city" : city,
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        rows = db.query(models.Data).filter(models.Data.city == city).with_entities(models.Data.aqi).all()
        aqis = [row[0] for row in rows]

        print(f"this is it: {aqis}")

        return aqis
    except Exception as e:
        logger.error(f"Could not get aqi for the city {city}")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting info about the aqi of this city - {e}")

def get_best_cities(db: Session):
    try:
        rows = db.query(models.Data.city, models.Data.aqi).all()

        if not rows:
            logger.error(f"There is no data about the aqis")
            raise HTTPException(status_code=404, detail="There is no data about the aqis")
        
        best_cities = sorted(rows, key=lambda x: x[1])[:3]

        print(best_cities)

        output = [{"city": city, "aqi": aqi} for city, aqi in best_cities]

        return output
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get aqis")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting info about the aqis")