import pytest
import requests
import os
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
    assert response.status_code == HTTPStatus.OK, f"Response was not 200. Reason: {response.reason}"
    return response.json().get("token", None)


@pytest.fixture
def booking_id() -> int:
    """
        Create new booking and getting its ID
    """
    payload = {
        "firstname": "John-Batman",
        "lastname": "Doe-Supermanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": (today + timedelta(days=1)).strftime("%Y-%m-%d"), 
            "checkout": (today + timedelta(days=11)).strftime("%Y-%m-%d")
        },
        "additionalneeds": "Dinner"
    }
    response = requests.post(config_parser.booking_endpoint, json=payload)
    assert response.status_code == HTTPStatus.OK, f"Response was not 200. Reason: {response.reason}"
    return response.json().get("bookingid", None)

def pytest_configure(config):
    html_option = config.option.htmlpath
    if html_option and not os.path.isabs(html_option):
        current_time = datetime.now().strftime("%H-%M %d-%m-%y")
        report_dir = "reports"
        new_filename = f"report-{current_time}.html"
        
        os.makedirs(report_dir, exist_ok=True)
        
        config.option.htmlpath = os.path.join(report_dir, new_filename)