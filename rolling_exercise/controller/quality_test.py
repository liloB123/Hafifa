import pytest
from unittest.mock import MagicMock, patch
from fastapi.exceptions import HTTPException
from quality_controller import get_qaulity_by_date, get_quality_by_city, insert_data_from_csv
from models import Data
import pandas as pd

ALERT_AQI = 100 

@pytest.fixture
def mock_db_session():
    mock_db = MagicMock()
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    return mock_db

######## insert data #######
@pytest.fixture
def mock_dataframe():
    data = {
        "date": ["2024-11-19", "2024-11-20"],
        "city": ["Tel Mond", "Hod Hasharon"],
        "PM2.5": [60, 20],
        "NO2": [30, 40],
        "CO2": [300, 400]
    }
    return pd.DataFrame(data)

@pytest.mark.asyncio
async def test_insert_data_from_csv_successful(mock_db_session, mock_dataframe):
    result = await insert_data_from_csv(mock_db_session, mock_dataframe)
    
    assert result["message"] == "Data added successfully!"

@pytest.mark.asyncio
async def test_insert_data_from_csv_db_error(mock_db_session, mock_dataframe):
    mock_db_session.commit.side_effect = Exception("Database error")
    
    with pytest.raises(HTTPException) as exc_info:
        await insert_data_from_csv(mock_db_session, mock_dataframe)
    
    assert exc_info.value.status_code == 500

######## city #######
def test_get_quality_by_city_success_several_instances(mock_db_session):
    mock_data = [Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=300),
        Data(date='2024-11-19', city="Hod Hasharon", pm25=20, co2= 300, aqi=500),
        Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=500)]
    
    city = "Tel Mond"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        data for data in mock_data if data.city == city
    ]

    alerts = get_quality_by_city(mock_db_session, city)
    assert len(alerts) == 2

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

def test_get_quality_by_city_success_one_instances(mock_db_session):
    mock_data = [Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=300)]
    
    city = "Tel Mond"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        data for data in mock_data if data.city == city
    ]

    alerts = get_quality_by_city(mock_db_session, city)
    assert len(alerts) == 1

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()


def test_get_quality_by_city_no_alerts(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    city = "Netanya"

    with pytest.raises(HTTPException) as exc_info:
        get_quality_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 404

def test_get_quality_by_city_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = "Netanya"
    
    with pytest.raises(HTTPException) as exc_info:
        get_quality_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 500

def test_get_quality_by_city_missing_city(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = None
    
    with pytest.raises(HTTPException) as exc_info:
        get_quality_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 422

######## date #######
def test_get_quality_by_date_success_several_instances(mock_db_session):
    mock_data = [Data(date='2024-11-10', city="Tel Mond", pm25=60, co2= 410, aqi=300),
        Data(date='2024-11-11', city="Hod Hasharon", pm25=20, co2= 300, aqi=500),
        Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=500)]

    start_date = "2024-11-10"
    end_date = "2024-11-12"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        data for data in mock_data if data.date >= start_date and data.date <= end_date
    ]

    alerts = get_qaulity_by_date(mock_db_session, start_date, end_date)
    assert len(alerts) == 2

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

def test_get_quality_by_date_success_one_instances(mock_db_session):
    mock_data = [Data(date='2024-11-10', city="Tel Mond", pm25=60, co2= 410, aqi=300),
        Data(date='2024-11-19', city="Hod Hasharon", pm25=20, co2= 300, aqi=500)]

    start_date = "2024-11-10"
    end_date = "2024-11-12"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        data for data in mock_data if data.date >= start_date and data.date <= end_date
    ]

    alerts = get_qaulity_by_date(mock_db_session, start_date, end_date)
    assert len(alerts) == 1

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

def test_get_quality_by_date_no_alerts(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    start_date = "2025-11-10"
    end_date = "2025-11-12"

    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 404

def test_get_quality_by_date_start_after_end_date(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-11-12"

    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Start date can not be later than end date"

def test_get_quality_by_date_not_valid_day(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-11-32"

    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

def test_get_quality_by_date_not_valid_month(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-15-14"

    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

def test_get_quality_by_date_not_valid_year(mock_db_session):
    start_date = "2025-11-13"
    end_date = "20251-11-14"

    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

def test_get_quality_by_date_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = "2025-11-13"
    end_date = "2025-11-14"
    
    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 500

def test_get_quality_by_date_missing_one_date(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = "2025-11-13"
    end_date = None
    
    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 422

def test_get_quality_by_date_missing_two_dates(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = None
    end_date = None
    
    with pytest.raises(HTTPException) as exc_info:
        get_qaulity_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 422
