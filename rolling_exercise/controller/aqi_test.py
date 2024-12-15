import pytest
from unittest.mock import MagicMock, patch
from fastapi.exceptions import HTTPException
from aqi_controller import get_aqi_by_city, get_aqi_average, get_best_cities
from models import Data

@pytest.fixture
def mock_db_session():
    return MagicMock()

####### city #######
@pytest.mark.asyncio
async def test_get_aqi_by_city_success(mock_db_session):
    mock_aqis = [Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=300), Data(date='2024-11-19', city="Hod Hasharon", pm25=20, co2= 300, aqi=500), Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=180)]

    city = "Tel Mond"

    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.return_value = [
        (alert.aqi,)
        for alert in mock_aqis if alert.city == city
    ]
    
    aqis = await get_aqi_by_city(mock_db_session, city)

    assert aqis == [300,180]

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_aqi_by_city_no_aqis(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.return_value = []

    city = "Netanya"

    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_aqi_by_city_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = "Netanya"
    
    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 500

@pytest.mark.asyncio
async def test_get_aqi_by_city_missing_city(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_by_city(mock_db_session, city)
    
    assert exc_info.value.status_code == 422

####### average #######
@pytest.mark.asyncio
async def test_get_aqi_average_success(mock_db_session):
    mock_aqis = [Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=300), Data(date='2024-11-19', city="Hod Hasharon", pm25=20, co2= 300, aqi=500), Data(date='2024-11-19', city="Tel Mond", pm25=60, co2= 410, aqi=500)]

    city = "Tel Mond"

    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.return_value = [
        (alert.aqi,)
        for alert in mock_aqis if alert.city == city
    ]
    
    aqis = await get_aqi_average(mock_db_session, city)

    assert aqis == 400

    mock_db_session.query.assert_called_once_with(Data)
    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.assert_called_once()

@pytest.mark.asyncio
async def test_get_aqi_average_no_aqis(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.with_entities.return_value.all.return_value = []

    city = "Netanya"

    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_average(mock_db_session, city)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_aqi_average_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = "Netanya"
    
    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_average(mock_db_session, city)
    
    assert exc_info.value.status_code == 500

@pytest.mark.asyncio
async def test_get_aqi_average_missing_city(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")

    city = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_aqi_average(mock_db_session, city)
    
    assert exc_info.value.status_code == 422

####### best #######
@pytest.mark.asyncio
async def test_get_best_cities_success(mock_db_session):
    mock_aqis = [
        ("Tel Mond", 300),
        ("Hod Hasharon", 500),
        ("Tel Mond", 500)
    ]
    
    mock_db_session.query.return_value.all.return_value = mock_aqis

    result = await get_best_cities(mock_db_session)

    sorted_data = sorted(mock_aqis, key=lambda x: x[1])[:3]
    expected_result = [{"city": city, "aqi": aqi} for city, aqi in sorted_data]

    assert result == expected_result

@pytest.mark.asyncio
async def test_get_best_cities_less_than_three_cities(mock_db_session):
    mock_aqis = [
        ("Tel Mond", 300),
        ("Tel Mond", 500),
    ]
    
    mock_db_session.query.return_value.all.return_value = mock_aqis

    result = await get_best_cities(mock_db_session)

    sorted_data = sorted(mock_aqis, key=lambda x: x[1])[:3]
    expected_result = [{"city": city, "aqi": aqi} for city, aqi in sorted_data]

    assert result == expected_result

@pytest.mark.asyncio
async def test_get_best_cities_more_than_three_cities(mock_db_session):
    mock_aqis = [
        ("Tel Mond", 300),
        ("Tel Mond", 500),
        ("Hod Hasharon", 500),
        ("Hod Hasharon", 300)
    ]
    
    mock_db_session.query.return_value.all.return_value = mock_aqis

    result = await get_best_cities(mock_db_session)

    sorted_data = sorted(mock_aqis, key=lambda x: x[1])[:3]
    expected_result = [{"city": city, "aqi": aqi} for city, aqi in sorted_data]

    assert result == expected_result

@pytest.mark.asyncio
async def test_get_best_cities_no_cities(mock_db_session):
    mock_db_session.query.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        await get_best_cities(mock_db_session)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_get_best_cities_db_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("Database error")
    
    with pytest.raises(HTTPException) as exc_info:
        await get_best_cities(mock_db_session)
    
    assert exc_info.value.status_code == 500


