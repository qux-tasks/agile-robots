import pytest
import requests
from etc import config_parser
from etc.helpers import build_booking_payload
from http import HTTPStatus


def test_create_booking_success():
    """
        Positive case to create a new booking
    """
    payload = build_booking_payload()
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, got reason: {response.reason}"
    body = response.json()

    assert "bookingid" in body, f"Response bode does not contain 'bookingid': {body}"
    assert isinstance(body["bookingid"], int), f"'bookingid' is not integer: {type(body["bookingid"])}"

    booking = body["booking"]
    assert booking["firstname"] == payload["firstname"], f"Expected firstname {payload['firstname']}, got {booking['firstname']}"
    assert booking["lastname"] == payload["lastname"], f"Expected lastname {payload['lastname']}, got {booking['lastname']}"
    assert booking["totalprice"] == payload["totalprice"], f"Expected totalprice {payload['totalprice']}, got {booking['totalprice']}"
    assert booking["depositpaid"] == payload["depositpaid"], f"Expected depositpaid {payload['depositpaid']}, got {booking['depositpaid']}"
    assert booking["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"], f"Expected checkin date {payload["bookingdates"]["checkin"]}, got {booking["bookingdates"]["checkin"]}"
    assert booking["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"], f"Expected checkout date {payload["bookingdates"]["checkout"]}, got {booking["bookingdates"]["checkout"]}"
    assert booking["additionalneeds"] == payload["additionalneeds"], f"Expected additionalneeds {payload['additionalneeds']}, got {booking['additionalneeds']}"

def test_create_booking_without_additionalneeds():
    """
        Case to create a booking without additionalneeds field
    """
    payload = build_booking_payload(additionalneeds=None)
    payload.pop("additionalneeds")
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, got reason: {response.reason}"
    body = response.json()
    assert "bookingid" in body, f"Response bode does not contain 'bookingid': {body}"
    assert "booking" in body, f"Response bode does not contain 'booking': {body}"
    assert "additionalneeds" not in body["booking"], f"Response bode contain 'additionalneeds': {body}"

def test_create_booking_with_accept_xml():
    """
        Case to create booking with Accept: application/xml
    """
    payload = build_booking_payload()
    headers = {"Accept": "application/xml", "Content-Type": "application/json"}
    response = requests.post(config_parser.booking_endpoint, json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Expected status code 200, got reason: {response.reason}"
    assert response.headers["Content-Type"].startswith("text/xml"), f"Not expected Content-Type: {response.headers["Content-Type"]}"

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
    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR], f"Unexpected status code: {response.status_code}"

@pytest.mark.parametrize("missing_field", ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"])
def test_create_booking_missing_required_fields(missing_field):
    """
        negative case with missing required fields
    """
    payload = build_booking_payload()
    payload.pop(missing_field)
    response = requests.post(config_parser.booking_endpoint, json=payload)

    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR], f"Unexpected status code: {response.status_code}"