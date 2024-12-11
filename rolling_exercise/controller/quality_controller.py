from sqlalchemy.orm import Session
import pandas as pd
import models
from fastapi import HTTPException
from functions import logger, calculate_aqi

ALERT_AQI = 300

def insert_data_from_csv(db: Session, df: pd.DataFrame):
    try:
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
            check_if_alert(db, date, city, aqi)

        db.commit()

        logger.info("New data was inserted to the database")
        return {"message": "Data added successfully!"}
    except Exception as e:
        logger.error(f"There has been a problem while trying to add data - {e}")
        raise HTTPException(status_code=400, detail="Could not upload the data")
    
def check_if_alert(db: Session, date, city, aqi):
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
        raise HTTPException(status_code=400, detail="Colud not add alert")
    

