from sqlalchemy.orm import Session
from app import models, schemas

def create_alert(db: Session, alert: schemas.AlertCreate):
    db_alert = models.Alert(date=alert.date, city=alert.city, aqi=alert.aqi)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alert(db: Session, alert_id: int):
    db_alert = db.query(models.Alert).filter(models.Alert.date == alert_id.date, models.Alert.city == alert_id.city).first()
    return db_alert
