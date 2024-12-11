from pydantic import BaseModel
from datetime import date
from typing import Optional

class DataBase(BaseModel):
    date: date
    city: str
    pm25: int
    no2: int
    co2: int
    aqi: float

class DataCreate(DataBase):
    pass

class Data(DataBase):
    class Config:
        orm_mode = True


class AlertBase(BaseModel):
    date: date
    city: str
    aqi: float

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    class Config:
        orm_mode = True
