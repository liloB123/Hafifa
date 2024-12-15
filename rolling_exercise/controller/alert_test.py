import pytest
from unittest.mock import MagicMock, patch
from fastapi.exceptions import HTTPException
from alert_controller import get_alerts, get_alerts_by_city, get_alerts_by_date
from models import Alert
import models

@pytest.fixture
def mock_db_session():
    return MagicMock()

####### alerts #######
@pytest.mark.asyncio
async def test_get_alerts_success(mock_db_session):
    mock_alerts = [Alert(date='2024-11-19', city="Tel Mond", aqi=300), Alert(date='2024-11-10', city="Netanya", aqi=500)]
    mock_db_session.query.return_value.all.return_value = mock_alerts

    alerts = await get_alerts(mock_db_session)

    assert alerts == mock_alerts

@pytest.mark.asyncio
async def test_get_alerts_no_alerts(mock_db_session):
    mock_db_session.query.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts(mock_db_session)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_alerts_db_error(mock_db_session, mocker):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts(mock_db_session)
    
    assert exc_info.value.status_code == 500

####### city #######
@pytest.mark.asyncio
async def test_get_alerts_by_city_success_several_instances(mock_db_session):
    mock_alerts = [
        Alert(date='2024-11-19', city="Netanya", aqi=300),
        Alert(date='2024-11-10', city="Netanya", aqi=500),
        Alert(date='2024-11-10', city="Tel Mond", aqi=500)
    ]

    city = "Netanya"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        alert for alert in mock_alerts if alert.city == city
    ]

    alerts = await get_alerts_by_city(mock_db_session, city)
    assert len(alerts) == 2

    mock_db_session.query.assert_called_once_with(models.Alert)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_alerts_by_city_success_one_instance(mock_db_session):
    mock_alerts = [
        Alert(date='2024-11-19', city="Netanya", aqi=300),
        Alert(date='2024-11-10', city="Tel Mond", aqi=500)
    ]

    city = "Netanya"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        alert for alert in mock_alerts if alert.city == city
    ]

    alerts = await get_alerts_by_city(mock_db_session, city)
    assert len(alerts) == 1

    mock_db_session.query.assert_called_once_with(models.Alert)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_alerts_by_city_no_alerts(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    city = "Netanya"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_alerts_by_city_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = "Netanya"
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 500

@pytest.mark.asyncio
async def test_get_alerts_by_city_missing_city(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 422

####### date #######
@pytest.mark.asyncio
async def test_get_alerts_by_date_success_several_instances(mock_db_session):
    mock_alerts = [
        Alert(date='2024-11-19', city="Netanya", aqi=300),
        Alert(date='2024-11-10', city="Netanya", aqi=500),
        Alert(date='2024-11-11', city="Tel Mond", aqi=500)
    ]

    start_date = "2024-11-10"
    end_date = "2024-11-12"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        alert for alert in mock_alerts if alert.date >= start_date and alert.date <= end_date
    ]

    alerts = await get_alerts_by_date(mock_db_session, start_date, end_date)
    assert len(alerts) == 2

    mock_db_session.query.assert_called_once_with(models.Alert)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_alerts_by_date_success_one_instances(mock_db_session):
    mock_alerts = [
        Alert(date='2024-11-19', city="Netanya", aqi=300),
        Alert(date='2024-11-11', city="Tel Mond", aqi=500)
    ]

    start_date = "2024-11-10"
    end_date = "2024-11-12"

    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        alert for alert in mock_alerts if alert.date >= start_date and alert.date <= end_date
    ]

    alerts = await get_alerts_by_date(mock_db_session, start_date, end_date)
    assert len(alerts) == 1

    mock_db_session.query.assert_called_once_with(models.Alert)
    mock_db_session.query.return_value.filter.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_alerts_by_date_no_alerts(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    start_date = "2025-11-10"
    end_date = "2025-11-12"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_alerts_by_date_start_after_end_date(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-11-12"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Start date can not be later than end date"

@pytest.mark.asyncio
async def test_get_alerts_by_date_not_valid_day(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-11-32"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

@pytest.mark.asyncio
async def test_get_alerts_by_date_not_valid_month(mock_db_session):
    start_date = "2025-11-13"
    end_date = "2025-15-14"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

@pytest.mark.asyncio
async def test_get_alerts_by_date_not_valid_year(mock_db_session):
    start_date = "2025-11-13"
    end_date = "20251-11-14"

    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Incorrect data format, should be YYYY-MM-DD"

@pytest.mark.asyncio
async def test_get_alerts_by_date_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = "2025-11-13"
    end_date = "2025-11-14"
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 500

@pytest.mark.asyncio
async def test_get_alerts_by_date_missing_one_date(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = "2025-11-13"
    end_date = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 422

@pytest.mark.asyncio
async def test_get_alerts_by_date_missing_two_dates(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    start_date = None
    end_date = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_alerts_by_date(mock_db_session, start_date, end_date)
    
    assert exc_info.value.status_code == 422


