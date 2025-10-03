import pytest
import requests
from etc import config_parser
from datetime import datetime, timedelta
from http import HTTPStatus


today = datetime.now().date()


@pytest.fixture(scope="session")
def auth_token() -> str:
    """
        Get new auth token for session
    """
    payload = {"username": config_parser.username, "password": config_parser.password}
    response = requests.post(config_parser.auth_endpoint, json=payload)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    return response.json().get("token", None)


@pytest.fixture
def booking_id() -> int:
    """
        Create new booking and getting its ID
    """
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": (today + timedelta(days=1)).strftime("%Y-%m-%d"), 
            "checkout": (today + timedelta(days=11)).strftime("%Y-%m-%d")
        },
        "additionalneeds": "Dinner"
    }
    response = requests.post(config_parser.booking_endpoint, json=payload)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200: {response.status_code}"
    return response.json().get("bookingid", None)