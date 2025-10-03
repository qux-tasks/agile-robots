import pytest
import requests
from etc import config_parser
from etc.helpers import build_booking_payload


def test_update_booking_success(auth_token, booking_id):
    """
        Positive case - successful update of booking
    """
    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == payload["firstname"]
    assert body["lastname"] == payload["lastname"]
    assert body["totalprice"] == payload["totalprice"]
    assert body["depositpaid"] == payload["depositpaid"]
    assert body["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert body["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]


def test_update_booking_without_auth(booking_id):
    """
        Negative case - update without auth
    """
    payload = build_booking_payload(firstname="Hacker")
    response = requests.put(f"{config_parser.booking_endpoint}/{booking_id}", json=payload)
    assert response.status_code == 403


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

    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == "Mike"


def test_update_booking_not_found(auth_token):
    """
        Negative case - update non-existent booking
    """
    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == 200
    existing_ids_length = len(get_all_booking_ids.json())

    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}", json=payload, headers=headers)
    assert response.status_code in [404, 405]


@pytest.mark.parametrize("field,value", [
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

    assert response.status_code in [400, 500]


@pytest.mark.parametrize("invalid_id", [0, -1])
def test_update_booking_edge_ids(auth_token, invalid_id):
    """
        Negative case - with edge case IDs
    """
    payload = build_booking_payload()
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}
    response = requests.put(f"{config_parser.booking_endpoint}/{invalid_id}", json=payload, headers=headers)

    assert response.status_code in [404, 405]