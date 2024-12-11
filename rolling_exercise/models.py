from sqlalchemy import Column, Integer, String, Date, Float, PrimaryKeyConstraint
from database import Base

class Data(Base):
    __tablename__ = "data"
    
    date = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    pm25 = Column(Integer, nullable=False)
    no2 = Column(Integer, nullable=False)
    co2 = Column(Integer, nullable=False)
    aqi = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('date', 'city'),
    )

class Alert(Base):
    __tablename__ = "alerts"

    date = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    aqi = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('date', 'city'),
    )
