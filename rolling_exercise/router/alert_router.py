from fastapi import APIRouter, Depends
from controller.alert_controller import get_alerts, get_alerts_by_date, get_alerts_by_city
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/", status_code=200)
def get_alerts_route(db: Session = Depends(get_db)):
    try:
        return get_alerts(db)
    except Exception as e:
        e

@router.get("/date", status_code=200)
def get_alerts_by_date_route(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        return get_alerts_by_date(db, start_date, end_date)
    except Exception as e:
        return e

@router.get("/city", status_code=200)
def get_alerts_by_city_route(city: str, db: Session = Depends(get_db)):
    try:
        return get_alerts_by_city(db, city)
    except Exception as e:
        return e