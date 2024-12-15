from sqlalchemy.orm import Session
import models
from functions import logger, validate_date, validate_query_params
from fastapi import HTTPException

async def get_alerts(db: Session):
    try:
        alerts = db.query(models.Alert).all()

        if alerts:
            logger.info(f"Got {len(alerts)} alerts")
            return alerts

        logger.error(f"There are no alerts")
        raise HTTPException(status_code=404, detail="There are no alerts")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get alerts")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting alerts - {e}")
    
async def get_alerts_by_date(db:Session, start:str, end:str):
    try:
        missing_params = validate_query_params({
            "start_date" : start,
            "end_date" : end
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
    
        validate_date(start, end)

        alerts = db.query(models.Alert).filter(models.Alert.date >= start, models.Alert.date <= end).all()

        if alerts:
            logger.info(f"{len(alerts)} rows were returned for the date range {start}-{end}")
            return alerts
        else:
            logger.error(f"There are no alerts in the date range {start}-{end}")
            raise HTTPException(status_code=404, detail="There are no alerts in this date range")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get alerts in the date range {start}-{end}")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting info about the alerts - {e}")

async def get_alerts_by_city(db: Session, city:str):
    try:
        missing_params = validate_query_params({
            "city" : city,
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        alerts = db.query(models.Alert).filter(models.Alert.city == city).all()

        if alerts:
            logger.info(f"{len(alerts)} alerts were returned of the city {city}")
            return alerts  
        
        logger.error(f"There are no alerts of the city {city}")
        raise HTTPException(status_code=404, detail="There are no alerts of this city")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get alerts for the city {city}")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting the alerts of the city - {e}")