from sqlalchemy.orm import Session
import pandas as pd
import models
from fastapi import HTTPException
from functions import logger, calculate_aqi, validate_date, validate_query_params
import datetime

ALERT_AQI = 300

async def insert_data_from_csv(db:Session, df:pd.DataFrame):
    try:
        print("hello")
        for _, row in df.iterrows():
            aqi = calculate_aqi(row['PM2.5'], row['NO2'], row['CO2'])[0]
            date=row['date']
            city=row['city']
            data = models.Data(
                date=date,
                city=city,
                pm25=row['PM2.5'],
                no2=row['NO2'], 
                co2=row['CO2'],
                aqi=aqi
            )
            db.add(data)
            await check_if_alert(db, date, city, aqi)

        db.commit()

        logger.info("New data was inserted to the database")
        return {"message": "Data added successfully!"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"There has been a problem while trying to add data - {e}")
        raise HTTPException(status_code=400, detail=f"Could not upload the data - {e}")
    
async def check_if_alert(db:Session, date, city, aqi):
    try:
        if aqi > ALERT_AQI:
            alert = models.Alert(
                date=date,
                city=city,
                aqi=aqi
            )

            db.add(alert)

            db.commit()
            logger.info(f"New alert was added for city {city} at date {date}")
    except Exception as e:
        logger.error(f"Could not add alert - {e}")
        raise HTTPException(status_code=500, detail="Colud not add alert")
    
async def get_qaulity_by_date(db:Session, start:str, end:str):
    try:
        missing_params = validate_query_params({
            "start_date" : start,
            "end-date" : end
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        validate_date(start, end)

        rows = db.query(models.Data).filter(models.Data.date >= start, models.Data.date <= end).all()

        if  rows:
            logger.info(f"{len(rows)} rows were returned for the date range {start}-{end}")
            return rows
        
        logger.error(f"There is no data about the date range {start}-{end}")
        raise HTTPException(status_code=404, detail="There is no data about this date range")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get air quality for the date range {start}-{end}")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting info about the date - {e}")
    
async def get_quality_by_city(db: Session, city:str):
    try:
        missing_params = validate_query_params({
            "city" : city,
        })

        if missing_params:
            raise HTTPException(status_code=422, detail=f"Missing query parameters: {', '.join(missing_params)}")
        
        rows = db.query(models.Data).filter(models.Data.city == city).all()

        if rows:
            logger.info(f"{len(rows)} rows were returned for the city {city}")
            return rows  
        
        logger.error(f"There is no data about the city {city}")
        raise HTTPException(status_code=404, detail="There is no data about this city")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Could not get air quality for the city {city}")
        raise HTTPException(status_code=500, detail=f"There has been a problem while getting info about the city - {e}")