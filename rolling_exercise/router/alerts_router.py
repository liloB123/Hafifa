from fastapi import APIRouter, Depends
from controller.alerts_controller import create_alert, get_alert
from app import schemas
from sqlalchemy.orm import Session
from database import get_db

# Initialize the router for alert routes
router = APIRouter()

# Route to create a new Alert
@router.post("/", response_model=schemas.Alert)
def create_alert_route(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    return create_alert(db=db, alert=alert)

# Route to get a specific Alert
@router.get("/{alert_id}", response_model=schemas.Alert)
def get_alert_route(alert_id: int, db: Session = Depends(get_db)):
    return get_alert(db=db, alert_id=alert_id)
