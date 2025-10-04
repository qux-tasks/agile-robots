import pytest
import requests
from etc import config_parser
from http import HTTPStatus


def test_partial_update_firstname_lastname(auth_token, booking_id):
    """
        Positive case - partial update of name and surname
    """
    payload = {"firstname": "James", "lastname": "Brown"}
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    response = requests.patch(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert body["firstname"] == "James", f"Booking firstname was not updated"
    assert body["lastname"] == "Brown", f"Booking lastname was not updated"

def test_partial_update_totalprice(auth_token, booking_id):
    """
        Positive case - partial update of total price
    """
    payload = {"totalprice": 555}
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    response = requests.patch(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert body["totalprice"] == 555, f"Booking totalprice was not updated"

def test_partial_update_without_auth(booking_id):
    """
        Negative case - partial update without auth
    """
    payload = {"firstname": "Hacker"}
    response = requests.patch(f"{config_parser.booking_endpoint}/{booking_id}", json=payload)

    assert response.status_code == HTTPStatus.FORBIDDEN, f"Unexpected status code: {response.status_code}"

def test_partial_update_with_basic_auth(booking_id):
    """
        Positive case - partial update with basic auth
    """
    payload = {"firstname": "Mike"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM=",
    }

    response = requests.patch(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    body = response.json()
    assert body["firstname"] == "Mike", f"Booking firstname was not updated with basic auth"

def test_partial_update_not_found(auth_token):
    """
        Negative case - partial update of non-existent booking
    """
    payload = {"firstname": "GhostBatman"}
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    get_all_booking_ids = requests.get(config_parser.booking_endpoint)
    assert get_all_booking_ids.status_code == HTTPStatus.OK, f"Response was not 200, got reason: {response.reason}"
    existing_ids_length = len(get_all_booking_ids.json())

    response = requests.patch(f"{config_parser.booking_endpoint}/{existing_ids_length + 99999999999}", json=payload, headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND, f"Unexpected status code: {response.status_code}"

@pytest.mark.skip(reason="Status code should be clarified: 400 or 500")
@pytest.mark.parametrize("field, value", [
    ("totalprice", "abc"),
    ("depositpaid", "yes"),
    ("bookingdates", {"checkin": "2023-99-99"}),
])
def test_partial_update_invalid_data(auth_token, booking_id, field, value):
    """
        Negative case - partial update with invalid data
    """
    payload = {field: value}
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    response = requests.patch(f"{config_parser.booking_endpoint}/{booking_id}", json=payload, headers=headers)
    assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR], f"Unexpected status code: {response.status_code}"

@pytest.mark.parametrize("invalid_id", [0, -1])
def test_partial_update_invalid_ids(auth_token, invalid_id):
    """
        Negative case - partial update with edge case IDs
    """
    payload = {"firstname": "Test"}
    headers = {"Content-Type": "application/json", "Cookie": f"token={auth_token}"}

    response = requests.patch(f"{config_parser.booking_endpoint}/{invalid_id}", json=payload, headers=headers)

    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.METHOD_NOT_ALLOWED], f"Unexpected status code: {response.status_code}"