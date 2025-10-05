import pytest
import requests
from etc import config_parser
from etc.helpers import build_booking_payload
from http import HTTPStatus


def test_update_booking_success(auth_token, booking_id):
    """
        Positive case - successful update of booking
    """
    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert body["firstname"] == payload["firstname"], f"Booking firstname was not updated: {body['firstname']}"
    assert body["lastname"] == payload["lastname"], f"Booking lastname was not updated: {body['lastname']}"
    assert body["totalprice"] == payload["totalprice"], f"Booking totalprice was not updated: {body['totalprice']}"
    assert body["depositpaid"] == payload["depositpaid"], f"Booking depositpaid was not updated: {body['depositpaid']}"
    assert body["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"], f"Booking checkin was not updated: {body['bookingdates']['checkin']}"
    assert body["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"], f"Booking checkout was not updated: {body['bookingdates']['checkout']}"

def test_update_booking_without_auth(booking_id):
    """
        Negative case - update without auth
    """
    payload = build_booking_payload(firstname="Hacker")
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload)
    assert response.status_code == HTTPStatus.FORBIDDEN, f"Unexpected status code: {response.status_code}"

def test_update_booking_with_basic_auth(booking_id):
    """
        Positive case - update with basic auth
    """
    payload = build_booking_payload(firstname="Mike")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="
    }
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert body["firstname"] == "Mike", f"Booking firstname was not updated with basic auth"

def test_update_booking_not_found(auth_token):
    """
        Negative case - update non-existent booking
    """
    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    existing_ids_length = len(get_all_booking_ids.json())

    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}", json=payload, headers=headers)
    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED], f"Unexpected status code: {response.status_code}"

@pytest.mark.skip(reason="Status code should be clarified: 400 or 500")
@pytest.mark.parametrize("field, value", [
    ("totalprice", "abc"),
    ("depositpaid", "not_bool"),
    ("bookingdates", {"checkin": "2023-99-99", "checkout": "2023-12-12"}),
])
def test_update_booking_invalid_data(auth_token, booking_id, field, value):
    """
        Negative case - update with invalid data
    """
    payload = build_booking_payload()
    payload[field] = value
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR], f"Unexpected status code: {response.status_code}"

@pytest.mark.parametrize("invalid_id", [0, -1])
def test_update_booking_edge_ids(auth_token, invalid_id):
    """
        Negative case - with edge case IDs
    """
    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{invalid_id}", json=payload, headers=headers)

    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED], f"Unexpected status code: {response.status_code}"