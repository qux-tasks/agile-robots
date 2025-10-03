import pytest
import requests
from etc import config_parser
from etc.helpers import build_booking_payload


def test_create_booking_success():
    """
        Positive case to create a new booking
    """
    payload = build_booking_payload()
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code == 200
    body = response.json()

    assert "bookingid" in body
    assert isinstance(body["bookingid"], int)

    booking = body["booking"]
    assert booking["firstname"] == payload["firstname"]
    assert booking["lastname"] == payload["lastname"]
    assert booking["totalprice"] == payload["totalprice"]
    assert booking["depositpaid"] == payload["depositpaid"]
    assert booking["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert booking["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
    assert booking["additionalneeds"] == payload["additionalneeds"]


def test_create_booking_without_additionalneeds():
    """
        Case to create a booking without additionalneeds field
    """
    payload = build_booking_payload(additionalneeds=None)
    payload.pop("additionalneeds")
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "bookingid" in body
    assert "booking" in body
    assert "additionalneeds" not in body["booking"]


def test_create_booking_with_accept_xml():
    """
        Case to create booking with Accept: application/xml
    """
    payload = build_booking_payload()
    headers = {"Accept": "application/xml", "Content-Type": "application/json"}
    response = requests.post(config_parser.booking_endpoint, json=payload, headers=headers)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/xml")


@pytest.mark.parametrize("field,value", [
    ("totalprice", "abc"),
    ("depositpaid", "not_boolean"),
    ("bookingdates", {"checkin": "2023-99-99", "checkout": "2023-12-12"}),
])
def test_create_booking_invalid_data(field, value):
    """
        Case with invalid data types for fields
    """
    payload = build_booking_payload()
    payload[field] = value
    response = requests.post(config_parser.booking_endpoint, json=payload)
    assert response.status_code in [400, 500]


@pytest.mark.parametrize("missing_field", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"])
def test_create_booking_missing_required_fields(missing_field):
    """
        negative case with missing required fields
    """
    payload = build_booking_payload()
    payload.pop(missing_field)
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code in [400, 500]